# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

# Standard Library
import logging

from .mixpanel_client import get_mixpanel_client

logger = logging.getLogger(__name__)
mp = get_mixpanel_client()


def track_user_registration(user):
    logger.info('Mixpanel: track_user_registration <user=%s>' % user.id)
    mp.people_set(user.id, {
        "$name": user.full_name,
        "$email": user.email,
        "$created": user.date_joined,
        "$first_interaction": user.first_interaction,
    })


def track_event_created(event):
    logger.info('Mixpanel: track_event_created <event=%s>' % event.id)
    mp.track(event.id, "Event Created", {
        "invitation_count": event.invitations_count,
        "event_date": event.event_date,
        "$distinct_id": event.owner.id,
    })
    mp.people_increment(event.owner.id, {
        'Total Event Created': 1,
        'Total Invitation Sent': event.invitations_count,
    })


def track_invitation_created(invitation):
    logger.info('Mixpanel: track_invitation_by_status <invitation=%s>' % invitation.id)
    mp.track(invitation.id, "Invitation Created", {
        "invitee_current_status": invitation.invitee_current_status,
        "invitation_created": invitation.created,
        "$distinct_id": invitation.invited_by.id,
    })
    mp.people_increment(invitation.invited_by.id, {
        'active_invitee': (invitation.invitee_current_status == 0).conjugate(),
        'passive_invitee': (invitation.invitee_current_status == 1).conjugate(),
        'new_user_invitee': (invitation.invitee_current_status == 2).conjugate(),
    })


def track_rsvp(invite):
    mp.track(invite.event.id, "Event RSVP", {
        "action": 'Yes' if invite.has_accepted_invite else 'No',
        "$distinct_id": invite.user.id
    })
