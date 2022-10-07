# -*- coding: utf-8 -*-
import os
import random

# Third Party Stuff
from django.conf import settings
from django.template import Context, Template

# Amigo Stuff
from amigo.notifications.services import send_bulk_push_notification, send_push_notification, send_sms
from amigo.notifications.models import EventToken
from amigo.events.models import Invitation, InviteText
from amigo.users.services import get_or_create_user
import re


# Event Reminder
# ------------------------------------------------------------------------------
def send_event_reminder_for_tomorrow(event, users):
    alert_str = '{ENV}{event_title} is happening tomorrow!'.format(event_title=event.title,
                                                                   ENV=settings.ENVIRONMENT)
    info = {
        'event_id': event.id,
        'type': 'reminder',
        'title': event.title,
    }
    return send_bulk_push_notification(users, alert=alert_str, info=info)


# Event RSVP
# ------------------------------------------------------------------------------
def send_invitation_rsvp_push_notification(event, user, rsvp_message=None):
    '''As an event creator, when someone accepts your invite you receive a push
    notification. This is listed in notifications setting as 'When an Amigo accepts my invite'.
    '''
    t = None
    ctx = Context({
        'user': user.get_short_name(),
        'rsvp_message': rsvp_message,
        'ENV': settings.ENVIRONMENT,
    })
    info = {
        'event_id': event.id,
        'type': 'rsvp',
        'title': event.title,
    }
    # Do not caclute it multiple times

    if event.owner.notify_invite_rsvp:
        t = Template('{% load humanize %}{{ENV}}{{user|safe}} responded with: {{ rsvp_message|safe }}.')

    if t:
        message_body = t.render(ctx)
        # add some sweetness!
        return send_push_notification(event.owner, alert=message_body, info=info)


def send_invitation_unattending_push_notification(event, user):
    if not event.owner.notify_invite_rsvp:
        return False

    t = Template('{% load humanize %}{{ENV}}{{user|safe}} can no longer make it.')
    message_body = t.render(Context({
        'user': user.get_full_name(),
        'ENV': settings.ENVIRONMENT,
    }))
    info = {
        'event_id': event.id,
        'type': 'rsvp',
        'title': event.title,
    }
    return send_push_notification(event.owner, alert=message_body, info=info)


# Event Invite
# ------------------------------------------------------------------------------
def send_invitation_push_notification(event, user):
    '''As an Amigo user, when an event creator invites me to an event I receive
    a push notification. This is listed in notifications setting as 'I receive a message'.
    '''
    if not user.notify_new_invite:
        return False

    message_body = '{ENV}{event_creator} invited you to: {event_title}.'.format(
        event_creator=event.owner.get_full_name(),
        event_title=event.title,
        ENV=settings.ENVIRONMENT
    )
    info = {
        'event_id': event.id,
        'type': 'invite',
        'title': event.title,
    }
    return send_push_notification(user, alert=message_body, info=info)


def linkify(text, maxlinklength=256):
    _urlfinderregex = re.compile(r'(http([^\.\s]|www)+\.[^\.\s]*)+[^\.\s]{2,}')

    def replacewithlink(matchobj):
        url = matchobj.group(0)
        text = unicode(url)
        if text.startswith('http://'):
            text = text.replace('http://', '', 1)
        elif text.startswith('https://'):
            text = text.replace('https://', '', 1)

        if text.startswith('www.'):
            text = text.replace('www.', '', 1)

        if len(text) > maxlinklength:
            halflength = maxlinklength / 2
            text = text[0:halflength] + '...' + text[len(text) - halflength:]

        return '<a href="' + url + '" target="_blank" rel="nofollow">' + text + '</a>'

    if text != '' and text is not None:
        return _urlfinderregex.sub(replacewithlink, text.lower())
    else:
        return ''


def send_invitation_sms(event, phone_number, inviter):
    user = get_or_create_user(phone_number=phone_number)

    try:
        Invitation.objects.get(event=event, user=user, invited_by=inviter)
    except Invitation.DoesNotExist:
        if user.is_app_user:
            Invitation.objects.create(event=event, user=user, invited_by=inviter)
        elif user.first_interaction:
            Invitation.objects.create(event=event, user=user, invited_by=inviter, invitee_current_status=1)
        else:
            Invitation.objects.create(event=event, user=user, invited_by=inviter, invitee_current_status=2)
    token = EventToken(user=user,
                       event=event)
    token.save_token()

    url = 'https://{}/invitation?token={}'.format(os.environ['DJANGO_SITE_DOMAIN'], token.token)
    all_invite_texts = list(InviteText.objects.all())
    random.shuffle(all_invite_texts)
    t = linkify(all_invite_texts[0].invite_text)

    message_body = t.format(organizer=event.owner.get_full_name().encode('utf-8'),
                            event_title=event.title,
                            event_link=url)
    return send_sms(to=user.phone_number, body=message_body)


def send_bulk_invitation_notification(invitations):

    # TODO: make this async?
    for invite in invitations:
        if invite.user.is_app_user:
            send_invitation_push_notification(invite.event, invite.user)
        if invite.phone_number:
            send_invitation_sms(invite.event, invite.phone_number, invite.invited_by)


# Event Change
# ------------------------------------------------------------------------------
def send_event_title_change_notification(event, users):
    t = '{ENV}{event_owner} has changed {event_title_old} to {event_title}.'
    return False
    alert_str = t.format(event_owner=event.owner.get_full_name(),
                         event_title=event.title,
                         event_title_old=event.tracker.previous('title'),
                         ENV=settings.ENVIRONMENT)
    info = {
        'event_id': event.id,
        'type': 'change',
        'title': event.title
    }

    return send_bulk_push_notification(users, alert=alert_str, info=info)


def send_event_time_change_notification(event, users):
    t = '{ENV}{event_owner} has changed the time of {event_title}. Can you still make it?'
    alert_str = t.format(event_owner=event.owner.get_full_name(),
                         event_title=event.title,
                         ENV=settings.ENVIRONMENT)
    info = {
        'event_id': event.id,
        'type': 'change',
        'title': event.title,
    }

    return send_bulk_push_notification(users, alert=alert_str, info=info)


def send_event_venue_change_notification(event, users):
    new_venue = event.venue_name.strip()
    if not new_venue:
        t = '{ENV}Heads up! {event_owner} has removed the location of {event_title}.'
    else:
        t = '{ENV}Heads up! {event_owner} has changed the location of {event_title} to {event_venue}.'
    return True
    alert_str = t.format(event_owner=event.owner.get_full_name(),
                         event_title=event.title,
                         event_venue=new_venue,
                         ENV=settings.ENVIRONMENT)
    info = {
        'event_id': event.id,
        'type': 'change',
        'title': event.title,
    }

    return send_bulk_push_notification(users, alert=alert_str, info=info)
