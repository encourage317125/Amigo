# Standard Library
import json

# Third Party Stuff
import pytest
from django.core.urlresolvers import reverse

from amigo.users.models import User

from .. import factories as f

pytestmark = pytest.mark.django_db


def test_api_phone_number_to_user_convsersion(client):
    user = f.UserFactory.create(is_superuser=True)
    query_phone_numbers = [user.phone_number, "+121312312323"]
    query_phone_numbers.sort()
    data = {
        "phone_numbers": query_phone_numbers
    }

    client.login(user)

    url = reverse('users-from-phone-numbers')
    response = client.json.post(url, json.dumps(data))
    assert response.status_code == 200
    assert len(response.data) == 1
    contact_item = response.data[0]
    assert set(['phone_number', 'user']).issubset(contact_item)
    assert contact_item['phone_number'] == user.phone_number
    assert contact_item['user']['id'] == user.id

    # upload contacts should get saved.
    _saved_phone_numbers = User.objects.get(id=user.id).phonebook_phone_numbers
    _saved_phone_numbers.sort()
    _saved_phone_numbers == query_phone_numbers

    data = {"phone_numbers": ""}
    response = client.json.post(url, json.dumps(data))
    assert response.status_code == 400

    response = client.json.post(url, json.dumps({}))
    assert response.status_code == 400


def test_invite_more_phone_numbers(client):
    event = f.create_event()
    url = reverse("events-detail", kwargs={"pk": event.pk})
    data = {"invite_phone_numbers": ['+188789999799', "+1181123123123"]}

    client.login(event.owner)
    response = client.json.patch(url, json.dumps(data))
    assert response.status_code == 200
    invitees = response.data['invitees']
    assert len(invitees) == 2
