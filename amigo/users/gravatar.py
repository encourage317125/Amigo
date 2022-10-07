# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

# Standard Library
import copy
import hashlib

# Third Party Stuff
from django.conf import settings

try:
    # Python 3
    from urllib.parse import urlencode
except (ImportError) as e:
    from urllib import urlencode


GRAVATAR_BASE_URL = "https://secure.gravatar.com/avatar/{}?{}"


def get_gravatar_url(email, **options):
    """Get the gravatar url associated to an email.

    :param options: Additional options to gravatar.
    - `default` defines what image url to show if no gravatar exists
    - `size` defines the size of the avatar.

    :return: Gravatar url.
    """

    params = copy.copy(options)

    default_avatar = getattr(settings, "GRAVATAR_DEFAULT_AVATAR", 'mm')
    default_size = getattr(settings, "GRAVATAR_AVATAR_SIZE", None)

    if default_avatar:
        params["default"] = default_avatar

    if default_size:
        params["size"] = default_size

    email_hash = hashlib.md5(email.lower().encode()).hexdigest()
    url = GRAVATAR_BASE_URL.format(email_hash, urlencode(params))

    return url
