# Standard Library
import json
from datetime import timedelta

# Third Party Stuff
import arrow
import pytest
from django.core.urlresolvers import reverse
from django.utils.functional import SimpleLazyObject
from django.utils.timezone import now
from django.test import Client
from mock import patch
from tests.utils import get_dict_from_list_where

from .. import factories as f

from amigo.notifications.models import EventToken

pytestmark = pytest.mark.django_db


@pytest.fixture
def user():
    return f.UserFactory.create()


def test_api_create_event(client, user):
    data = {
        "title": "Dinner @ my place",
        "event_date": arrow.utcnow().isoformat(),
        "invite_phone_numbers": ["+09897999989"],
    }

    url = reverse('events-list')
    client.login(user)

    response = client.json.post(url, json.dumps(data))
    assert response.status_code == 201
    assert response.data['i_am_owner'] is True
    assert set(['i_am_attending', 'owner', 'invitees', 'my_rsvp_message', 'venue_name']).issubset(response.data.keys())
    assert 'invite_phone_numbers' not in response.data.keys()
    assert 'invitees_photos' not in response.data.keys()
    assert response.data['my_rsvp_message'] is None
    assert 'invitees' in response.data.keys()
    assert response.data['is_time_specified'] is True

    # should accept optional `is_time_specified` and store it
    data = {
        "title": "Dinner @ my place",
        "event_date": arrow.utcnow().isoformat(),
        "invite_phone_numbers": ["+09897999989"],
        "is_time_specified": False,
    }
    response = client.json.post(url, json.dumps(data))
    assert response.data['is_time_specified'] is False

    # should accept optional `location` and `address` and store it
    data = {
        "title": "Dinner @ my place",
        "event_date": arrow.utcnow().isoformat(),
        "invite_phone_numbers": ["+09897999989"],
        "location": {
            "latitude": 23.8,
            "longitude": 89
        },
        "address": "Broadway\nNYC",
        "venue_name": "Pizza Place"
    }
    response = client.json.post(url, json.dumps(data))
    assert response.data['address'] == data['address']
    assert response.data['location'] == data['location']
    assert response.data['venue_name'] == data['venue_name']


def test_api_invite_registerd_user_while_event_creations(client, user):
    user2 = f.UserFactory.create()
    data = {
        "title": "Dinner @ my place",
        "event_date": arrow.utcnow().isoformat(),
        "invite_phone_numbers": [user2.phone_number],
    }

    url = reverse('events-list')
    client.login(user)

    response = client.post(url, json.dumps(data), content_type="application/json")
    assert response.status_code == 201

    invitees = response.data.get('invitees', None)
    assert len(invitees) == 1
    assert get_dict_from_list_where(invitees, 'phone_number', user2.phone_number)['is_active'] is True


def test_api_invite_non_registerd_user_while_event_creations(client, user):
    data = {
        "title": "Dinner @ my place",
        "event_date": arrow.utcnow().isoformat(),
        "invite_phone_numbers": ["+9000920234234"],
    }

    url = reverse('events-list')
    client.login(user)

    response = client.post(url, json.dumps(data), content_type="application/json")
    invitees = response.data.get('invitees', None)

    assert invitees is not None
    assert len(invitees) == 1
    assert get_dict_from_list_where(invitees, 'phone_number', "+9000920234234")['is_active'] is False
    assert 'faded_photo' in invitees[0].keys()


def test_api_invite_user_while_event_creations(client, user):
    user2 = f.UserFactory.create()
    data = {
        "title": "Dinner @ my place",
        "event_date": arrow.utcnow().isoformat(),
        "invite_phone_numbers": ["+9000920234234", user2.phone_number],
    }

    url = reverse('events-list')
    client.login(user)

    response = client.post(url, json.dumps(data), content_type="application/json")

    invitees = response.data.get('invitees', None)
    assert invitees is not None
    assert len(invitees) == 2

    response = client.json.get(url)
    result = response.data.get('results', None)
    assert len(result) == 1


def test_api_partially_update_event(client):
    event = f.create_event()
    url = reverse("events-detail", kwargs={"pk": event.pk})
    data = {"title": ""}

    client.login(event.owner)
    response = client.json.patch(url, json.dumps(data))
    assert response.status_code == 400

    data = {"title": "some other title"}
    response = client.json.patch(url, json.dumps(data))
    assert response.status_code == 200

    data = {"event_date": arrow.utcnow().replace(hours=+2).isoformat()}
    response = client.json.patch(url, json.dumps(data))
    assert response.status_code == 200

    data = {
        "location": {
            "latitude": 0,
            "longitude": 89
        }
    }
    response = client.json.patch(url, json.dumps(data))
    assert response.status_code == 200
    assert response.data['location'] == data["location"]


def test_api_list_events(client):
    event = f.EventFactory.create()

    url = reverse('events-list')
    client.login(event.owner)

    response = client.json.get(url)
    assert response.status_code == 200

    # Check that list is paginated
    assert set(['count', 'next', 'previous', 'results']).issubset(response.data.keys())
    results = response.data.get('results', None)
    assert results is not None
    assert len(results) == 1

    # list view shouldn't have 'invitees' in it.
    event = results[0]
    assert 'invitees' in event.keys()
    assert 'my_rsvp_message' in event.keys()
    should_not_be_present = ['invitees_count', 'attendees_count', "i_have_seen"]
    for key in should_not_be_present:
        assert key not in response.data.keys()
    assert isinstance(event['invitees'], list)
    assert len(event['invitees']) == 0


def test_i_am_owner_filter(client):
    event = f.EventFactory.create()

    url = reverse('events-list')
    client.login(event.owner)

    response = client.json.get(url + '?i_am_owner=True')
    assert response.status_code == 200
    assert response.data['count'] == 1

    response = client.json.get(url + '?i_am_owner=false')
    assert response.status_code == 200
    assert response.data['count'] == 0


def test_api_detail_event(client):
    event = f.EventFactory.create()

    url = reverse("events-detail", kwargs={"pk": event.pk})
    client.login(event.owner)

    response = client.json.get(url)
    assert response.status_code == 200
    invitees = response.data.get('invitees', None)
    assert len(invitees) == 0
    should_not_be_present = ['invitees_count', 'attendees_count', "i_have_seen"]
    for key in should_not_be_present:
        assert key not in response.data.keys()


def test_api_cancel_event(client):
    event = f.EventFactory.create()
    url = reverse("events-cancel-event", kwargs={"pk": event.pk})

    client.login(event.owner)
    response = client.json.put(url)
    assert response.status_code == 204


def test_ios_event_inivitation_page(client):
    owner = f.UserFactory()
    event = f.EventFactory.create(owner=owner)
    invitation = f.AttendeeFactory(event=event, invited_by=owner)
    evt_token = EventToken(user=owner, event=event, token="123")
    evt_token.save()

    client.login(invitation.user)
    client = Client(HTTP_USER_AGENT="Mozilla/5.0 (iPhone; CPU iPhone OS 9_2 like Mac OS X) "
                                    "AppleWebKit/601.1.46 (KHTML, like Gecko) "
                                    "Version/9.0 Mobile/13B143 Safari/601.1")
    response = client.get(reverse("pages:invitation") + "?token=123")

    assert response.status_code == 200
    assert response.context['event'] == event
    assert response.context['map_link'] == 'http://maps.apple.com/?q='


def test_android_event_inivitation_page(client):
    owner = f.UserFactory()
    event = f.EventFactory.create(owner=owner)
    invitation = f.AttendeeFactory(event=event, invited_by=owner)
    evt_token = EventToken(user=owner, event=event, token="123")
    evt_token.save()

    client.login(invitation.user)
    client = Client(HTTP_USER_AGENT="Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) "
                                    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/"
                                    "48.0.2564.23 Mobile Safari/537.36")
    response = client.get(reverse("pages:invitation") + "?token=123")

    assert response.status_code == 200
    assert response.context['event'] == event
    assert response.context['map_link'] == 'http://maps.google.com/?q='


def test_event_inivitation_calendar(client):
    owner = f.UserFactory()
    event = f.EventFactory.create(owner=owner)
    invitation = f.AttendeeFactory(event=event, invited_by=owner)
    evt_token = EventToken(user=owner, event=event, token="123")
    evt_token.save()

    client.login(invitation.user)
    response = client.get(reverse("pages:invitation_calendar") + "?token=123")

    assert response.status_code == 200
    assert response['content-type'] == 'text/calendar'


def test_inivitation_with_rsvp_msg(client):
    owner = f.UserFactory()
    event = f.EventFactory.create(owner=owner)
    invitation = f.AttendeeFactory(event=event, invited_by=owner)
    evt_token = EventToken(user=owner, event=event, token="123")
    evt_token.save()

    client.login(invitation.user)
    client = Client(HTTP_USER_AGENT="Mozilla/5.0 (iPhone; CPU iPhone OS 9_2 like Mac OS X) "
                                    "AppleWebKit/601.1.46 (KHTML, like Gecko) "
                                    "Version/9.0 Mobile/13B143 Safari/601.1")
    response = client.post(reverse("pages:invitation") + "?token=123",
                           {"response": "Accept",
                            "rsvp-message": "Foo RSVP msg"})

    assert response.status_code == 200


def test_event_accept(client):
    owner = f.UserFactory()
    event = f.EventFactory.create(owner=owner)
    invitation = f.AttendeeFactory(event=event, invited_by=owner)

    url = reverse("events-accept", kwargs={"pk": event.pk})
    client.login(invitation.user)
    data = {}

    event_url = reverse("events-detail", kwargs={"pk": event.pk})
    response = client.get(event_url, content_type="application/json")
    assert response.data['i_am_attending'] is None

    response = client.post(url, json.dumps(data), content_type="application/json")
    assert response.status_code == 200
    assert response.data['i_am_attending'] is True

    event_url = reverse("events-detail", kwargs={"pk": event.pk})
    response = client.get(event_url, content_type="application/json")
    assert response.data['i_am_attending'] is True

    with patch("amigo.events.services.mark_user_as_attending") as attend_service:
        attend_service.return_value = True
        response = client.json.post(url, json.dumps(data))
        attend_service.assert_called_once_with(event=event, user=SimpleLazyObject(lambda: invitation.user),)
        # should be called with rsvp_message when it is present
        data = {
            "rsvp_message": "I'll be there!"
        }
        response = client.json.post(url, json.dumps(data))
        attend_service.assert_called_with(event=event, user=SimpleLazyObject(lambda: invitation.user),
                                          rsvp_message=data["rsvp_message"])


def test_event_my_rsvp_message(client):
    owner = f.UserFactory()
    event = f.EventFactory.create(owner=owner)
    invitation = f.AttendeeFactory(event=event, invited_by=owner)
    url = reverse("events-accept", kwargs={"pk": event.pk})
    client.login(invitation.user)
    data = {
        "rsvp_message": "I'll be there!"
    }
    response = client.json.post(url, json.dumps(data))

    event_url = reverse("events-detail", kwargs={"pk": event.pk})
    response = client.json.get(event_url)
    assert response.data['i_am_attending'] is True
    assert response.data['my_rsvp_message'] == data['rsvp_message']


def test_event_reject(client):
    owner = f.UserFactory()
    event = f.EventFactory.create(owner=owner)
    invitation = f.AttendeeFactory(event=event, has_accepted_invite=True, invited_by=owner)

    url = reverse("events-reject", kwargs={"pk": event.pk})
    client.login(invitation.user)
    data = {}

    event_url = reverse("events-detail", kwargs={"pk": event.pk})
    response = client.json.get(event_url)
    assert response.data['i_am_attending'] is True

    response = client.json.post(url, json.dumps(data))
    assert response.status_code == 200
    assert response.data['i_am_attending'] is False

    event_url = reverse("events-detail", kwargs={"pk": event.pk})
    response = client.json.get(event_url)
    assert response.data['i_am_attending'] is False

    with patch("amigo.events.services.mark_user_as_unattending") as unattend_service:
        unattend_service.return_value = True
        response = client.json.post(url, json.dumps(data))
        unattend_service.assert_called_once_with(event=event, user=SimpleLazyObject(lambda: invitation.user),)
        # should be called with rsvp_message when it is present
        data = {
            "rsvp_message": "Sorry!"
        }
        response = client.json.post(url, json.dumps(data))
        unattend_service.assert_called_with(event=event, user=SimpleLazyObject(lambda: invitation.user),
                                            rsvp_message=data["rsvp_message"])


def test_filter_old_events(client):
    expired_event_date = arrow.utcnow().replace(hours=-10)
    event = f.EventFactory.create(event_date=expired_event_date.datetime)

    after_date = arrow.utcnow().replace(hours=-5).timestamp
    client.login(event.owner)

    url = reverse("events-list")

    # check for event_after filter
    filtered_url = url + '?event_after=%s' % after_date

    response = client.json.get(filtered_url)
    assert response.status_code == 200
    assert response.data['count'] == 0

    invalid_filtered_url = url + '?event_after=%s' % 'bla bla'
    response = client.json.get(invalid_filtered_url)
    assert response.status_code == 200
    assert response.data['count'] == 1

    # check for event_before filter
    before_date = arrow.utcnow().replace(hours=-14).timestamp
    filtered_url = url + '?event_before=%s' % before_date
    response = client.json.get(filtered_url)
    assert response.status_code == 200
    assert response.data['count'] == 0

    event_url = reverse("events-detail", kwargs={"pk": event.pk})
    response = client.get(event_url, content_type="application/json")
    assert response.status_code == 200


def test_api_event_stats(client):
    url = reverse("events-stats")
    owner = f.UserFactory()
    user = f.UserFactory()
    event = f.EventFactory.create(event_date=now() + timedelta(hours=2), owner=owner)
    f.InvitationFactory.create(user=user, event=event, has_accepted_invite=None, invited_by=owner)

    # should require auth
    response = client.json.get(url)
    assert response.status_code == 401

    client.login(user)

    response = client.json.get(url)
    assert response.status_code == 200
    assert response.data['unresponded_invite_count'] == 1
