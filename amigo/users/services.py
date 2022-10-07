# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

# Standard Library
import random

# Third Party Stuff
from django.apps import apps
from django.conf import settings
from django.utils.timezone import now

# Amigo Stuff
from amigo.base.utils.urls import get_absolute_url
from amigo.notifications.services import send_sms

from . import utils
from .gravatar import get_gravatar_url


def get_or_create_user(phone_number, full_name=None, photo=None, app_user=False):
    user_model = apps.get_model("users", "User")
    qs = user_model.objects.filter(phone_number=phone_number)
    if len(qs) == 0:
        return user_model.objects.create_user(phone_number=phone_number,
                                              full_name=full_name,
                                              photo_uri=photo,
                                              is_active=False,
                                              is_app_user=False)
    user = qs[0]
    user.last_login = now()
    user.save()

    return user


def get_or_make_inactive_user(phone_number, app_user=False):
    '''
    Check if user with phone_number exists, else create an inactive user.

    password is set as something predictable for future usuages.
    '''
    user_model = apps.get_model("users", "User")
    qs = user_model.objects.filter(phone_number=phone_number)

    # Create a random password for phone number validation
    password = ''.join(["%s" % random.randint(0, 9) for num in range(0, settings.SMS_VALIDATION_LENGTH)])
    send_sms(phone_number, settings.SMS_VALIDATION_MESSAGE.format(password, password))

    if len(qs) == 0:
        return user_model.objects.create_user(phone_number=phone_number,
                                              is_active=False,
                                              password=password,
                                              is_app_user=app_user)
    user = qs[0]
    user.last_login = now()
    user.set_password(password)
    user.save()

    return user


def __get_photo_url(photo, big=False):
    """Get a photo absolute url and the photo automatically cropped."""

    try:
        size_opt = settings.DEFAULT_BIG_AVATAR_SIZE if big else settings.DEFAULT_AVATAR_SIZE
        size = '{size}x{size}'.format(size=size_opt)
        url = photo.crop[size].url
        return get_absolute_url(url)
    except IOError:
        return None


def get_faded_photo_url(photo):
    """Get a photo absolute url and the photo automatically cropped."""
    try:
        size = '{size}x{size}'.format(size=settings.DEFAULT_AVATAR_SIZE)
        url = photo.filters.fade.crop[size].url
        return get_absolute_url(url)
    except IOError:
        return None


def get_photo_or_gravatar_url(user):
    """Get the user's photo/gravatar url."""
    if user:
        return __get_photo_url(user.photo) if user.photo else get_gravatar_url(user.email)
    return ""


def get_photo_or_none(user):
    """Get the user's photo/none url."""
    if user:
        return __get_photo_url(user.photo) if user.photo else None
    return None


def get_big_photo_or_gravatar_url(user):
    """Get the user's big photo/gravatar url."""
    if user:
        return __get_photo_url(user.photo, big=True) if user.photo \
            else get_gravatar_url(user.email, size=settings.DEFAULT_BIG_AVATAR_SIZE)
    return ""


def get_big_photo_or_none(user):
    """Get the user's big photo/none."""
    if user:
        return __get_photo_url(user.photo, big=True) if user.photo else None
    return None


def get_faded_photo_or_none(user):
    """Get the user's faded photo/none."""
    if user:
        return get_faded_photo_url(user.photo) if user.photo else None
    return None


def get_contacts_and_associated_user(owner, **filters):
    '''
    Returns a list of all `FavoriteContact` objects of the given `owner`, along with
    partial user object with matching the phone_number, if present.

    `id__in` can used to filter contacts to return only in these ids.
    '''
    contacts_query = utils.left_join_contact_and_user(owner, **filters)

    def convert_to_obj(_contact):
        Contact = apps.get_model("users", "FavoriteContact")
        contact = Contact(
            id=_contact.id,
            phone_number=_contact.phone_number,
            created=_contact.created,
        )
        contact.user = None
        if _contact.user_id:
            user_model = apps.get_model("users", "User")
            contact.user = user_model(id=_contact.user_id,
                                      full_name=_contact.user_full_name,
                                      photo=_contact.user_photo,
                                      is_active=_contact.user_is_active)
        return contact

    return map(convert_to_obj, contacts_query)


def get_owners_of_phone_number(phone_number):
    user_model = apps.get_model('users', 'User')
    return user_model.objects.filter(phonebook_phone_numbers__contains=phone_number)


def add_favorite_in_bulk(user, phone_numbers):
    contact_model = apps.get_model('users', 'FavoriteContact')
    for phone_number in phone_numbers:
        contact, created = contact_model.objects.get_or_create(phone_number=phone_number, owner=user)
