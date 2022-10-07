# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

# Third Party Stuff
from django.conf import settings

# Amigo Stuff
from amigo.notifications.services import send_bulk_push_notification
from amigo.users.serializers import UserSerializer
from amigo.users.services import get_owners_of_phone_number

from .backends import get_token_for_user


def send_new_contact_joined_notification(user):
    '''
    Send notification to all the users where the phone number of this user is
    present.
    '''
    alert_str = '{ENV}Oooh, {name} just joined Amigo, they copy everything you do, amiright?'.format(
        name=user.get_short_name(),
        ENV=settings.ENVIRONMENT)
    info = {
        "type": "new_user",
        "user_id": user.id
    }
    users = get_owners_of_phone_number(user.phone_number)
    users_to_notify = [u for u in users if u.notify_contact_joined]
    return send_bulk_push_notification(users_to_notify, alert=alert_str, info=info)


def make_auth_response_data(user):
    """
    Given a domain and user, creates data structure
    using python dict containing a representation
    of the logged user.
    """
    serializer = UserSerializer(user)
    data = dict(serializer.data)
    data["auth_token"] = get_token_for_user(user)
    return data
