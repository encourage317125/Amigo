# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

# Amigo Stuff
from amigo.events.models import Event, Invitation


def _get_user_event_invite(user, event):
    if user.is_anonymous():
        return None

    try:
        return Invitation.objects.get(user=user, event=event)
    except Invitation.DoesNotExist:
        return None


def _get_object_event(obj):
    event = None

    if isinstance(obj, Event):
        event = obj
    elif obj and hasattr(obj, 'event'):
        event = obj.event
    return event


def is_event_owner(user, obj):
    if user.is_superuser:
        return True

    event = _get_object_event(obj)

    if event and event.owner == user:
        return True

    invitee = _get_user_event_invite(user, event)
    if invitee and invitee.is_owner:
        return True

    return False


def is_event_attending(user, obj):

    event = _get_object_event(obj)

    if event and event.owner == user:
        return True

    invitee = _get_user_event_invite(user, event)
    if invitee and invitee.is_owner:
        return True

    if invitee:
        return invitee.has_accepted_invite

    return False


def get_event_rsvp_message(user, event):
    invite = _get_user_event_invite(user, event)
    if invite:
        return invite.rsvp_message
    return None
