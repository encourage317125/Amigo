# Third Party Stuff
import pytest
from django.core.urlresolvers import reverse
from tests.utils import get_dict_from_list_where

from .. import factories as f

pytestmark = pytest.mark.django_db


def test_api_invite_to_unregistered_user(client):
    owner = f.UserFactory()
    event = f.EventFactory.create(owner=owner)
    phone_number = '+9199999123123'

    # create an invitation on this number
    f.InvitationFactory.create(event=event, phone_number=phone_number, invited_by=owner)

    # a user registers with this number
    user = f.UserFactory.create(phone_number=phone_number, is_active=True)

    # he should get a event in his events feed.
    url = reverse('events-list')
    client.login(user)
    response = client.json.get(url)
    assert response.status_code == 200
    results = response.data.get('results', None)
    assert results is not None
    assert len(results) == 1
    assert results[0]['i_am_owner'] is False

    url = reverse("events-detail", kwargs={"pk": event.pk})
    response = client.json.get(url)

    invitees = response.data.get('invitees', None)
    assert len(invitees) == 1
    invited_user = get_dict_from_list_where(invitees, 'phone_number', phone_number)

    assert set(['photo', 'big_photo', 'rsvp_message', 'rsvp_time', 'created']).issubset(invited_user.keys())
    assert invited_user['full_name'] == user.full_name
    assert invited_user['rsvp_time'] is None

    assert get_dict_from_list_where(invitees, 'phone_number', event.owner.phone_number) is None


def test_api_all_users_who_has_invited_me(client):

    user = f.UserFactory()
    owner1 = f.UserFactory()
    owner2 = f.UserFactory()
    event1 = f.EventFactory.create(owner=owner1)
    event2 = f.EventFactory.create(owner=owner2)

    # create two invitation
    invite1 = f.InvitationFactory.create(event=event1, user=user, invited_by=owner1)
    invite2 = f.InvitationFactory.create(event=event2, user=user, invited_by=owner2)
    # TODO: What is the purpose of the dummy factory?
    # f.InvitationFactory.create()  # dummy

    # i should be able to get all the users who has invited me
    url = reverse('users-who-has-invited-me')
    client.login(user)
    response = client.json.get(url)
    assert response.status_code == 200
    assert len(response.data) == 2
    assert [response.data[0]['id'], response.data[1]['id']].sort() == \
           [invite1.invited_by.id, invite2.invited_by.id].sort()


def test_sample_rsvp_replies_list(client):
    url = reverse('events-sample-rsvp-replies')
    user = f.UserFactory()
    client.login(user)

    response = client.json.get(url)
    assert response.status_code == 200
    assert len(response.data) == 0

    f.SampleRSVPReplyFactory.create_batch(2, type='accept')
    f.SampleRSVPReplyFactory.create_batch(1, type='reject')

    response = client.json.get(url)
    assert response.status_code == 200
    assert len(response.data) == 3

    item = response.data[0]
    assert set(['id', 'text', 'type']).issubset(item.keys())
