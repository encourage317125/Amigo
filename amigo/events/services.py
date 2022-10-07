# -*- coding: utf-8 -*-
# Standard Library
from datetime import timedelta

# Third Party Stuff
from django.apps import apps
from django.conf import settings
from django.core.cache import cache
from django.utils.timezone import now

# Amigo Stuff
from amigo.analytics import services as analytics_services
from amigo.base.utils.cache import get_cache_key
from amigo.users.services import get_photo_or_none
from amigo.users.services import get_or_create_user

from . import notification_services

ENV = '[%s] ' % settings.ENVIRONMENT if settings.ENVIRONMENT else ''


def get_invited_users(event, **extra_filters):
    '''Returns all the registered users who are invited to an event, it excluded
    the owner of the event.'''
    invitation_model = apps.get_model("events", "Invitation")
    qs = invitation_model.objects.filter(event=event)
    qs = qs.filter(is_owner=False).exclude(user__isnull=True)
    qs = qs.select_related('user')

    if extra_filters:
        qs = qs.filter(**extra_filters)

    return [invite.user for invite in qs]


def get_unresponded_invitations(user):
    invitation_model = apps.get_model("events", "Invitation")
    qs = invitation_model.objects.upcoming()
    qs = qs.filter(user=user)
    qs = qs.filter(has_accepted_invite=None)
    return qs


def get_invitees_photo_urls(event, max_users=10):
    cache_key = get_cache_key('event_invitee_photo_urls', event_id=event.id)
    invitee_photo_urls = cache.get(cache_key)
    if invitee_photo_urls is not None:
        return invitee_photo_urls

    # Not found in cache, retrieve from database and return after setting the cache
    invitation_model = apps.get_model("events", "Invitation")
    invitations_qs = invitation_model.objects.filter(event=event)
    invitations_qs = invitations_qs.filter(is_owner=False).exclude(user__isnull=True)
    invitations_qs = invitations_qs.select_related('user')
    invitations_qs = invitations_qs[:max_users]
    invitee_photo_urls = [get_photo_or_none(invite.user) for invite in invitations_qs]
    cache.set(cache_key, invitee_photo_urls, timeout=None)  # cache forever
    return invitee_photo_urls


def associate_user_to_invites(user):
    invitation_model = apps.get_model("events", "Invitation")
    return invitation_model.objects.filter(phone_number=user.phone_number).update(user=user)


def mark_user_as_attending(event, user, rsvp_message=None):
    """
    Find the invitation of user in the given event and mark that invitation being attended
    also update the user object if it's not present.

    Returns the event object.
    """
    invitation_model = apps.get_model("events", "Invitation")
    invitation = invitation_model.objects.filter(event=event, user=user).first()

    if not invitation:
        return False

    if invitation.has_accepted_invite and rsvp_message:
        invitation.rsvp_message = rsvp_message
        invitation.has_accepted_invite = True
        invitation.has_seen = True
        invitation.rsvp_time = now()
        invitation.save()
        notification_services.send_invitation_rsvp_push_notification(event=event,
                                                                     user=user,
                                                                     rsvp_message=rsvp_message)
        return invitation.event

    lock_key = "event:%s:attend-lock" % event.id
    with cache.lock(lock_key):
        invitation.has_accepted_invite = True
        invitation.has_seen = True
        invitation.rsvp_message = rsvp_message
        invitation.rsvp_time = now()
        invitation.save()

    notification_services.send_invitation_rsvp_push_notification(event=event,
                                                                 user=user,
                                                                 rsvp_message=rsvp_message)
    analytics_services.track_rsvp(invitation)
    return invitation.event


def mark_user_as_unattending(event, user, rsvp_message=None):
    """
    Find the invitation of user in the given event and mark that invitation being
    unattending.

    Returns the event object.
    """
    invitation_model = apps.get_model("events", "Invitation")
    invitation = invitation_model.objects.filter(event=event, user=user).first()

    if not invitation:
        return False

    invitation.has_accepted_invite = False
    invitation.rsvp_message = rsvp_message
    invitation.rsvp_time = now()
    invitation.save()
    notification_services.send_invitation_unattending_push_notification(event, user)
    analytics_services.track_rsvp(invitation)
    return invitation.event


def mark_as_seen(event, user):
    invitation_model = apps.get_model("events", "Invitation")
    return invitation_model.objects.filter(event=event, user=user).update(has_seen=True)


def add_bulk_invitation_by_phone(event, invitees, invited_by):
    user_model = apps.get_model("users", "User")
    invitation_model = apps.get_model("events", "Invitation")

    phone_numbers = [d['phone'] for d in invitees]

    # exclude phone_numbers which are already invited.
    invited_phone_numbers = invitation_model.objects.filter(event=event, phone_number__in=phone_numbers) \
                                            .values_list('phone_number', flat=True)
    phone_numbers = list(set(phone_numbers) - set(invited_phone_numbers))

    # users that already exist with given phone numbers
    users = user_model.objects.filter(phone_number__in=phone_numbers)

    invitations = []
    phone_numbers_added = []

    for user in users:
        phone_numbers_added.append(user.phone_number)
        invitations.append(
            invitation_model(event=event, user=user, phone_number=user.phone_number,
                             invited_by=invited_by))

    non_user_phone_numbers = set(phone_numbers) - set(phone_numbers_added)

    # Updated invitations so that it tracks the users interaction with the app at the
    # time of the invitation being sent.
    for phone_number in non_user_phone_numbers:
        invitee = next(invitee for invitee in invitees if invitee['phone'] == phone_number)
        user = get_or_create_user(phone_number=invitee['phone'], full_name=invitee['name'], photo=invitee['photo'])
        if user.first_interaction:
            invitations.append(
                invitation_model(user=user, event=event, phone_number=phone_number,
                                 invited_by=invited_by, invitee_current_status=invitation_model.PASSIVE_USER))
        else:
            invitations.append(
                invitation_model(user=user, event=event, phone_number=phone_number,
                                 invited_by=invited_by, invitee_current_status=invitation_model.NEW_USER))

    # The model’s save() method will not be called, and the pre_save and post_save
    # signals will not be sent.
    invitation_model.objects.bulk_create(invitations)

    # bulk_create doesn't call signals, so clear invitee photo urls cache here
    cache_key = get_cache_key('event_invitee_photo_urls', event_id=event.id)
    cache.delete(cache_key)

    notification_services.send_bulk_invitation_notification(invitations)


def sent_event_reminders():
    # let's a window of 1hr with cron running every 1/2 hour
    Event = apps.get_model("events", "Event")

    # send event happening tomorrow reminder
    qs = Event.objects.all()
    qs = qs.filter(event_date__lt=now() + timedelta(hours=26))
    qs = qs.exclude(event_date__lt=now() + timedelta(hours=24))
    qs = qs.exclude(reminder_sent=True)

    for event in qs:
        send_to = get_invited_users(event, has_accepted_invite=True, user__notify_upcoming_event=True)
        notification_services.send_event_reminder_for_tomorrow(event, send_to)

    qs.update(reminder_sent=True)
