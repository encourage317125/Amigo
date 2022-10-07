# -*- coding: utf-8 -*-
# Third Party Stuff
import pytest
from mock import patch

# Amigo Stuff
from amigo.users.services import get_owners_of_phone_number, \
    get_photo_or_gravatar_url, get_big_photo_or_gravatar_url, \
    get_faded_photo_or_none, get_photo_or_none, \
    get_big_photo_or_none

from .. import factories as f

pytestmark = pytest.mark.django_db


def test_get_owners_of_phone_number():
    user = f.UserFactory.create(phonebook_phone_numbers=["+918377086100"])
    result = get_owners_of_phone_number("+918377086100")
    assert len(result) == 1
    assert result[0].id == user.id


def test_get_photo_or_gravatar_url():
    user = f.UserFactory.create()
    photo_url = get_photo_or_gravatar_url(user)
    assert photo_url is not None
    photo_url = get_photo_or_gravatar_url(None)
    assert photo_url == ""


def test_get_big_photo_or_gravatar_url():
    user = f.UserFactory.create()
    # photo = f.django.ImageField(color='blue')
    photo_url = get_big_photo_or_gravatar_url(user)
    assert photo_url is not None

    with patch('amigo.users.services.get_gravatar_url', return_value="foo.png"):
        user.photo = None
        photo_url = get_big_photo_or_gravatar_url(user)
        assert photo_url == 'foo.png'


def test_get_photo_none():
    assert get_photo_or_none(None) is None
    assert get_big_photo_or_none(None) is None
    assert get_faded_photo_or_none(None) is None
    assert get_big_photo_or_gravatar_url(None) == ""


def test_get_faded_photo_or_none():
    user = f.UserFactory.create()
    photo_url = get_faded_photo_or_none(user)
    assert photo_url is not None


def test_photo_url_io_error():
    user = f.UserFactory.create()
    with patch('versatileimagefield.datastructures.base.ProcessedImage.retrieve_image', side_effect=IOError):
        result = get_faded_photo_or_none(user)
        assert result is None
        result = get_big_photo_or_gravatar_url(user)
        assert result is None
