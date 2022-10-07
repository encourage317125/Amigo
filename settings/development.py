# -*- coding: utf-8 -*-
''' Development Configurations

Adds sensible defaults for developement of project
- Enables DEBUG
- Outputs outgoing emails to console
- Enables Django Debug Toolbar
- Uses local caches
'''
from __future__ import absolute_import, unicode_literals

# Third Party Stuff

from .common import *  # noqa


class Development(Common):
    DEBUG = env.bool('DJANGO_DEBUG', default=True)
    TEMPLATE_DEBUG = DEBUG

    # SECRET CONFIGURATION
    # ------------------------------------------------------------------------------
    # A secret key for this particular Django installation. Used in secret-key
    # hashing algorithms. Set this in your settings, or Django will complain
    # loudly.
    # See: https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
    # Note: This key only used for development and testing.
    SECRET_KEY = env("DJANGO_SECRET_KEY", default='CHANGEME!!!')\

    ALLOWED_HOSTS = ['127.0.0.1']  # allows testing for DEBUG=False locally

    # Mail settings
    EMAIL_HOST = "localhost"
    EMAIL_PORT = 1025
    EMAIL_BACKEND = env('DJANGO_EMAIL_BACKEND',
                        default='django.core.mail.backends.console.EmailBackend')
    # End mail settings

    SITE_ID = 'local'

    Common.AIRBRAKE['ENVIRONMENT'] = 'development'
