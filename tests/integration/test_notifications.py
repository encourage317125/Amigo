# -*- coding: utf-8 -*-

# Standard Library
import json
from mock import patch, MagicMock

# Third Party Stuff
import pytest
from django.core.urlresolvers import reverse
from zeropush.models import PushDevice

from .. import factories as f

pytestmark = pytest.mark.django_db


def test_apple_device_registration(client):
    user = f.create_user()
    user2 = f.create_user()
    token = "06fa8ae3b8ee0206ab4518771269544b6c173ba5ca6eadbc1e19ab1b7d1e779f"

    data = {
        "token": token
    }

    url = reverse('notifications-add-ios-device')
    with patch("amigo.notifications.services.get_mixpanel_client", return_value=MagicMock()) as fake_mp:
        response = client.post(url, json.dumps(data), content_type="application/json")
        assert response.status_code == 401

        client.login(user)

        response = client.post(url, json.dumps(data), content_type="application/json")
        assert response.status_code == 200
        assert fake_mp.people_union.called_once_with(user.id,
                                                     {u'$ios_devices': [token]})

        response = client.post(url, json.dumps(data), content_type="application/json")
        assert response.status_code == 200
        assert response.data['user_id'] == user.id

        client.logout()

        # if a second guys, login on the same device,
        client.login(user2)
        data = {"token": token}
        response = client.json.post(url, json.dumps(data))
        assert response.status_code == 200
        assert response.data['user_id'] == user2.id


def test_api_remove_device(client):
    user = f.create_user()

    url = reverse("notifications-remove-ios-device")

    data = {}

    response = client.json.post(url, json.dumps(data))
    assert response.status_code == 401

    client.login(user)
    response = client.json.post(url, json.dumps(data))
    assert response.status_code == 400

    data = {
        "token": "a" * 64
    }
    # this device is not registered yet
    response = client.json.post(url, json.dumps(data))
    assert response.status_code == 200
    assert response.data['success'] is False

    # now register the device
    url_add_device = reverse("notifications-add-ios-device")
    response = client.json.post(url_add_device, json.dumps(data))
    assert response.status_code == 200

    response = client.json.post(url, json.dumps(data))
    assert response.status_code == 200
    assert response.data['success'] is True
    assert response.data['user_id'] == user.id

    # disconnect again
    response = client.json.post(url, json.dumps(data))
    assert response.status_code == 200
    PushDevice.objects.all().count() == 0
