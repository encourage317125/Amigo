# -*- coding: utf-8 -*-
# Third Party Stuff
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured


def get_cache_key(key, **kwargs):
    try:
        CACHE_KEY_TEMPLATE = settings.CACHE_KEYS[key]
    except (AttributeError, KeyError):
        raise ImproperlyConfigured("'%s' key not found in 'CACHE_KEYS' dict inside settings" % key)

    return CACHE_KEY_TEMPLATE.format(**kwargs)
