# -*- coding: utf-8 -*-

# Standard Library
from datetime import timedelta

# Third Party Stuff
import pytest
from django.core.exceptions import ValidationError
from django.utils.timezone import now
from freezegun import freeze_time

# Amigo Stuff
from amigo.events.models import Event, Invitation
from amigo.events.services import add_bulk_invitation_by_phone, get_unresponded_invitations, mark_user_as_attending

from .. import factories as f

pytestmark = pytest.mark.django_db


@pytest.fixture
def event():
    return f.EventFactory.create()


def test_event_creation():
    user = f.UserFactory.create()
    event = f.EventFactory.create(owner=user)

    assert Event.objects.count() == 1
    assert event.owner == user


def test_event_add_bulk_invitation_by_phone():
    users = f.UserFactory.create_batch(2)

    invitor = f.UserFactory()
    event = f.EventFactory.create(owner=invitor)

    phone_numbers = [x.phone_number for x in users]
    add_bulk_invitation_by_phone(event, phone_numbers, invitor)

    # check if user Invitations are created
    assert Invitation.objects.filter(event=event).count() == len(users)

    # check user is assigned to a invitation if an amigo user exist in the set
    # of phone numbers
    user_invite = Invitation.objects.filter(event=event, user=users[0])
    assert user_invite.count() == 1
    assert user_invite[0].has_accepted_invite is None


def test_bulk_invite_duplicate_numbers():

    invitor = f.UserFactory()
    event = f.EventFactory.create(title='new event', owner=invitor)
    # should be able to handle duplicate numbers
    phone_numbers = ['+111111111111', '+111111111111', '+2222222222']
    add_bulk_invitation_by_phone(event, phone_numbers, invitor)
    assert Invitation.objects.filter(event=event).count() == 2


def test_bulk_invite_reinvite(event):
    user = f.UserFactory.create()

    invitor = f.UserFactory()

    # should be able to handle multiple numbers
    phone_numbers = [user.phone_number, '+111111111111']
    add_bulk_invitation_by_phone(event, phone_numbers, invitor)
    assert Invitation.objects.filter(event=event).count() == 2

    phone_numbers = [user.phone_number, '+111111111111']
    add_bulk_invitation_by_phone(event, phone_numbers, invitor)
    assert Invitation.objects.filter(event=event).count() == 2


def test_invite_accept():
    owner = f.UserFactory.create()
    second_user = f.UserFactory.create()

    event = f.EventFactory.create(owner=owner)
    invitation = f.AttendeeFactory.create(event=event, user=second_user, invited_by=owner)
    invitation.clean()  # TODO: avoid this
    invitation.save()  # TODO: avoid this

    mark_user_as_attending(event, second_user)

    # confirm that user has accepted the invite
    second_user_invitation = Invitation.objects.get(event=event, user=second_user)
    assert second_user_invitation.has_accepted_invite is True
    assert second_user_invitation.has_seen is True
    assert second_user_invitation.rsvp_time is not None


def test_multiple_invite_accept_and_change_spots():
    owner = f.UserFactory.create()
    invitees = f.UserFactory.create_batch(6)

    event = f.EventFactory.create(owner=owner)
    for user in invitees:
        invitation = f.AttendeeFactory.create(event=event, user=user, invited_by=owner)
        invitation.clean()  # TODO: avoid this
        invitation.save()  # TODO: avoid this
        mark_user_as_attending(event, user)

    # confirm that the users has accepted the invite
    for user in invitees:
        user_invitation = Invitation.objects.get(event=event, user=user, invited_by=owner)
        assert user_invitation.has_accepted_invite is True

    try:
        event.clean()
        event.save()
    except Exception as e:
        assert isinstance(e, ValidationError)


def test_cancel_event():
    owner = f.UserFactory.create()
    event = f.EventFactory.create(owner=owner)
    event.cancel()
    assert event.is_canceled is True


@freeze_time("2014-01-15 06:00:00", tz_offset=0)
def test_unresponsded_invitations():
    owner = f.UserFactory.create()
    user = f.UserFactory()
    event = f.EventFactory.create(event_date=now() + timedelta(hours=2), owner=owner)
    invite = f.InvitationFactory.create(user=user, event=event, has_accepted_invite=None, invited_by=owner)

    assert get_unresponded_invitations(user).count() == 1

    # should return no invite is it's responded
    invite.has_accepted_invite = True
    invite.save()
    assert get_unresponded_invitations(user).count() == 0

    # now user get invited to another event
    owner2 = f.UserFactory.create()
    event2 = f.EventFactory.create(event_date=now() + timedelta(hours=1), owner=owner2)
    invite2 = f.InvitationFactory.create(user=user, event=event2, has_accepted_invite=None, invited_by=owner2)
    assert get_unresponded_invitations(user).count() == 1

    # should not consider event today with time and but happening in past.
    invite2.event.event_date = now() - timedelta(hours=3)
    invite2.event.is_time_specified = True
    invite2.event.save()
    assert get_unresponded_invitations(user).count() == 0

    # should consider event within 12hours in past with no time.
    invite2.event.event_date = now() - timedelta(hours=6)
    invite2.event.is_time_specified = False
    invite2.event.save()
    assert get_unresponded_invitations(user).count() == 1

    # should not consider beyoud 12hr with no time.
    invite2.event.event_date = now() - timedelta(hours=25)
    invite2.event.is_time_specified = False
    invite2.event.save()
    assert get_unresponded_invitations(user).count() == 0

    # should consider event withing 2hr in past with time
    invite2.event.event_date = now() - timedelta(hours=1)
    invite2.event.is_time_specified = True
    invite2.event.save()
    assert get_unresponded_invitations(user).count() == 1

    # should not consider event beyond 2hr in past with time
    invite2.event.event_date = now() - timedelta(hours=3)
    invite2.event.is_time_specified = True
    invite2.event.save()
    assert get_unresponded_invitations(user).count() == 0
