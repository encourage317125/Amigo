# Standard Library
import json
from tempfile import NamedTemporaryFile

# Third Party Stuff
import pytest
from django.core.urlresolvers import reverse
from django.utils import six
from mock import patch, MagicMock
from facebook import GraphAPIError

from .. import factories as f

pytestmark = pytest.mark.django_db


def test_api_user_normal_user(client):
    user = f.UserFactory.create(is_superuser=True)
    data = {}

    url = reverse('users-list')
    response = client.post(url, json.dumps(data), content_type="application/json")
    assert response.status_code == 401

    client.login(user)

    response = client.post(url, json.dumps(data), content_type="application/json")
    assert response.status_code == 405


def test_user_details(client):
    user = f.create_user(email='user@example.com', photo=None)
    client.login(user)
    url = reverse("users-detail", kwargs={"pk": user.pk})
    response = client.json.get(url)
    assert response.status_code == 200

    assert set(['photo', 'big_photo']).issubset(response.data.keys())
    assert response.data['photo'] is None
    assert response.data['big_photo'] is None


def test_user_change_info(client):
    user = f.create_user()
    data = {
        "email": "new@example.com"
    }

    client.login(user)

    url = reverse("users-detail", kwargs={"pk": user.pk})
    response = client.json.patch(url, json.dumps(data))
    assert response.status_code == 200
    assert response.data['email'] == "new@example.com"

    data = {
        "full_name": "My Name"
    }

    response = client.json.patch(url, json.dumps(data))
    assert response.status_code == 200
    assert response.data['full_name'] == "My Name"


DUMMY_BMP_DATA = b'BM:\x00\x00\x00\x00\x00\x00\x006\x00\x00\x00(\x00\x00\x00\x01\x00\x00\x00\x01\x00\x00\x00\x01\x00\x18\x00\x00\x00\x00\x00\x04\x00\x00\x00\x13\x0b\x00\x00\x13\x0b\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'  # noqa


def test_change_avatar(client):
    url = reverse('users-change-avatar')

    user = f.UserFactory()
    client.login(user)

    with NamedTemporaryFile() as avatar:
        # Test no avatar send
        post_data = {}
        response = client.post(url, post_data)
        assert response.status_code == 400

        # Test invalid file send
        post_data = {
            'photo': avatar
        }
        response = client.post(url, post_data)
        assert response.status_code == 400

        # Test valid avatar send
        avatar.write(DUMMY_BMP_DATA)
        avatar.seek(0)
        response = client.post(url, post_data)
        assert response.status_code == 200
        assert isinstance(response.data['photo'], six.string_types)
        assert isinstance(response.data['big_photo'], six.string_types)


@patch('amigo.users.serializers.GraphAPI')
def test_register_fb_token(MockGraphAPI, client):
    url = reverse('users-register-fb-token')

    user = f.UserFactory()
    client.login(user)

    post_data = {}
    response = client.post(url, post_data)
    assert response.status_code == 400

    # Test valid facebook token
    post_data = {
        'fb_token': 'valid_token'
    }
    MockGraphAPI.return_value.get_object = MagicMock(return_value={'email': u'wei@amigo.io',
                                                                   'first_name': u'Amigo',
                                                                   'id': u'187108548350151',
                                                                   'last_name': u'Gonzales',
                                                                   'picture': {'data': {'is_silhouette': False,
                                                                                        'url': 'https://fbcdn.net/v'}}})

    response = client.post(url, post_data)
    assert response.status_code == 200
    MockGraphAPI.assert_called_once_with(access_token='valid_token', version='2.5')
    # print response.data
    assert response.data['full_name'] == 'Amigo Gonzales'
    assert response.data['photo'] is not None
    assert '.jpg' in response.data['photo']

    # Test invalid facebook token
    post_data = {
        'fb_token': 'invalid_token'
    }
    MockGraphAPI.return_value.get_object = MagicMock(side_effect=GraphAPIError('invalid fb token'))

    response = client.post(url, post_data)
    assert response.status_code == 400
    assert response.data == "Invalid Facebook access token"


@patch('amigo.users.api.GraphAPI')
def test_fb_friends(MockGraphAPI, client):
    url = reverse('users-fb-friends')

    user = f.UserFactory()
    client.login(user)
    response = client.get(url)
    assert response.status_code == 400
    assert response.data == "No Facebook access token provided"

    # Test valid token
    user.fb_token = 'valid_token'
    user.save()
    client.login(user)
    MockGraphAPI.return_value.get_connections = MagicMock(
            return_value={'data': [{'name': 'friend 1', 'id': 'f_1'}]})
    response = client.get(url)
    assert response.status_code == 200
    assert 'friend 1' in response.content

    # Test invalid token
    MockGraphAPI.return_value.get_connections = MagicMock(side_effect=GraphAPIError('invalid fb token'))
    response = client.get(url)
    assert response.status_code == 400
    assert response.data == "Invalid Facebook access token"
