# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# Third Party Stuff
from django.apps import apps


def left_join_contact_and_user(owner):
    # Use raw_sql until orm level functions are available.
    contact_model = apps.get_model('users', 'FavoriteContact')
    raw_query = 'SELECT c.id, c.phone_number, c.created, ' \
                'u.id as user_id, u.full_name as user_full_name, ' \
                'u.photo as user_photo, u.is_active as user_is_active ' \
                'FROM users_favoritecontact c ' \
                'LEFT JOIN users_user u ON (c.phone_number = u.phone_number) ' \
                'WHERE c.owner_id = %(owner_id)s '
    params = {
        'owner_id': owner.id,
    }

    return contact_model.objects.raw(raw_query, params)
