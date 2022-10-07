# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import random

# Standard Library
import json

# Third Party Stuff
import pytest
from django.core.urlresolvers import reverse

from .. import factories as f
from ..utils import disconnect_signals, reconnect_signals

from amigo.events.models import Event

pytestmark = pytest.mark.django_db


def setup_module(module):
    disconnect_signals()


def teardown_module(module):
    reconnect_signals()


@pytest.fixture
def user():
    return f.UserFactory.create(is_active=False)


def test_auth_create(client, user):
    url = reverse('auth-list')

    login_data = json.dumps({
        "phone_number": user.phone_number
    })

    result = client.json.post(url, login_data)
    assert result.status_code == 204

    login_data_new_user = json.dumps({
        "phone_number": "+09897990089"
    })

    result = client.json.post(url, login_data_new_user)
    assert result.status_code == 204

    login_data_new_user = json.dumps({
        "phone_number": "+09897990022"
    })

    # test more than user creation.
    result = client.json.post(url, login_data_new_user)
    assert result.status_code == 204


def test_auth_two_or_more_create(client, user):
    url = reverse('auth-list')

    phone_numbers = ["+9897990089", "+9897990023"]

    for ph in phone_numbers:
        login_data_new_user = json.dumps({
            "phone_number": ph
        })

        result = client.json.post(url, login_data_new_user)
        assert result.status_code == 204


def test_auth_action_register(client, settings, mocker):
    settings.PUBLIC_REGISTER_ENABLED = True
    track_user_registration = mocker.patch('amigo.analytics.services.track_user_registration')
    send_new_contact_joined_notification = mocker.patch('amigo.auth.services.send_new_contact_joined_notification')
    url = reverse('auth-register')

    user = f.UserFactory.create(full_name="My name with 😈",
                                phone_number="+9897990023")

    register_data = {
        "full_name": user.full_name,
        "email": user.email,
    }

    result = client.json.post(url, json.dumps(register_data))

    # Unauthenticated
    assert result.status_code == 401

    client.login(user)

    result = client.json.post(url, json.dumps(register_data))
    assert result.status_code == 200
    assert result.data['is_active'] is True
    assert result.data['full_name'] == user.full_name
    assert result.data['notify_new_invite'] is True
    assert result.data['notify_invite_rsvp'] is True
    assert result.data['notify_contact_joined'] is True
    assert result.data['notify_event_full'] is True
    assert result.data['notify_upcoming_event'] is True

    track_user_registration.called_once_with(user)
    send_new_contact_joined_notification.called_once_with(user)


def test_pin_verification(client, user):
    f.create_user(phone_number='+14155555678', full_name='Amigo Team', password='fdsa')
    url = reverse('auth-verify-pin')

    # Set the pin
    pin = random.randint(1000, 9999)
    user.set_password(pin)
    user.save()

    data = {
        'pin': '0000',
        'phone_number': user.phone_number
    }

    result = client.json.post(url, json.dumps(data))

    # Wrong pin.
    assert result.status_code == 400

    # Set the correct pin
    data['pin'] = pin

    result = client.json.post(url, json.dumps(data))

    assert result.status_code == 200
    assert result.data['is_active'] is True
    assert 'auth_token' in result.data.keys()

    # Test if pin is made invalid.
    result = client.json.post(url, json.dumps(data))

    assert result.status_code == 400

    # Ensure user has sample received events
    assert user.events.all().count() == 1
    # Ensure user has sent sample events
    assert Event.objects.filter(owner=user).count() == 1


def test_debug_pin_verification(client, user):
    f.create_user(phone_number='+14155555678', full_name='Amigo Team', password='fdsa')
    url = reverse('auth-verify-pin')

    debug_pin = '1111'

    data = {
        'pin': debug_pin,
        'phone_number': user.phone_number
    }

    result = client.json.post(url, json.dumps(data))
    assert result.status_code == 200
    assert result.data['is_active'] is True
    assert 'auth_token' in result.data.keys()


def test_auth_login(client, user):
    # Check Unauthorized if no valid token in header
    url = reverse('api-root')
    result = client.json.get(url)

    assert result.status_code == 401

    # Get auth-token from Login Endpoint
    url = reverse('auth-list')
    login_data = json.dumps({
        "phone_number": user.phone_number
    })

    result = client.json.post(url, login_data)
    assert result.status_code == 204
