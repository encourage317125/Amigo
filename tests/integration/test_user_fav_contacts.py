# Standard Library
import json

# Third Party Stuff
import pytest
from django.core.urlresolvers import reverse


from .. import factories as f
from ..utils import get_dict_from_list_where

pytestmark = pytest.mark.django_db


def test_fetch_contacts(client):
    url = reverse('users-favorite-contacts')
    user = f.create_user()

    f.FavoriteContactFactory.create_batch(2, owner=user)

    # should require authenticated user
    response = client.json.get(url)
    assert response.status_code == 401

    client.login(user)

    response = client.json.get(url)
    assert response.status_code == 200
    assert len(response.data) == 2
    item = response.data[0]
    assert set(["id", "phone_number", "user", "is_favorite"]).issubset(item.keys())
    assert item['is_favorite'] is True

    # should not display other users' contact book
    user2 = f.create_user()
    f.FavoriteContactFactory.create_batch(1, owner=user2)
    response = client.json.get(url)
    assert response.status_code == 200
    assert len(response.data) == 2

    # should connect user object when user with same phone number exist
    user_new = f.create_user(phone_number="+911177080000")
    _contact = f.FavoriteContactFactory.create(owner=user, phone_number=user_new.phone_number)
    response = client.json.get(url)
    assert response.status_code == 200
    assert len(response.data) == 3
    contact = get_dict_from_list_where(response.data, 'id', _contact.id)
    assert contact['user']['id'] == user_new.id


def test_add_remove_favorite_contacts(client):
    url = reverse('users-favorite-contacts')
    user = f.create_user()
    # should require authenticated user
    response = client.json.get(url)
    assert response.status_code == 401

    client.login(user)
    data = {
        "phone_numbers": ["+911177080000"]
    }
    response = client.json.post(url, json.dumps(data))
    assert response.status_code == 200

    assert "+911177080000" in response.content

    # should return one item when favorite contact is fetched.
    response = client.json.get(url)
    assert len(response.data) == 1

    # should remove from favorite contact when DELETE/PATCH is called.
    response = client.json.patch(url, json.dumps(data))
    assert response.status_code == 204

    # should return no item when favorite contact is fetched.
    response = client.json.get(url)
    assert len(response.data) == 0
