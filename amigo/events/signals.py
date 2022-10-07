# -*- coding: utf-8 -*-
# Third Party Stuff
from django.core.cache import cache

# Amigo Stuff
from amigo.analytics.services import track_event_created, track_invitation_created
from amigo.base.utils.cache import get_cache_key

from . import models, notification_services, services


# Signals for Invitation
# ----------------------------------------------------
def clear_event_invitation_caches(sender, instance, created, **kwargs):
    invitation = instance

    if created:
        cache_key_photos = get_cache_key('event_invitee_photo_urls', event_id=invitation.event.id)
        cache.delete(cache_key_photos)


def track_new_invitation_created(sender, instance, created, **kwargs):
    if created:
        track_invitation_created(instance)


# Signals for Event
# ----------------------------------------------------
def track_new_event_created(sender, instance, created, **kwargs):
    if created:
        track_event_created(instance)


def add_event_owner_in_attendee_list(sender, instance, created, **kwargs):
    event = instance

    if created:
        # add event owner in attendee in attendee list
        invite, created = models.Invitation.objects.get_or_create(
            user=event.owner, event=event)
        invite.is_owner = True
        invite.has_accepted_invite = True
        invite.has_seen = True
        invite.invited_by = event.owner
        invite.phone_number = event.owner.phone_number
        invite.save()


def notify_event_detail_change(sender, instance, created, **kwargs):
    event = instance

    if created:
        return False

    attending_users = services.get_invited_users(event, has_accepted_invite=True)

    if event.tracker.has_changed('title'):
        notification_services.send_event_title_change_notification(event, attending_users)

    if event.tracker.has_changed('event_date'):
        notification_services.send_event_time_change_notification(event, attending_users)

    if event.tracker.has_changed('venue_name'):
        notification_services.send_event_venue_change_notification(event, attending_users)
