# Standard Library
import logging

# Third Party Stuff
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from mixpanel import Mixpanel
from mixpanel_async import AsyncBufferedConsumer
from mock import Mock

logger = logging.getLogger(__name__)


def get_mixpanel_client(PROJECT_TOKEN=None):
    '''
    Returns properly configured Mixpanel instance, if PROJECT_TOKEN is not
    found and DEBUG=True, it retuns an instance of Mock() suitable for testing.
    '''
    if not PROJECT_TOKEN:
        PROJECT_TOKEN = getattr(settings, 'MIXPANEL_PROJECT_TOKEN', None)

    if PROJECT_TOKEN:
        return Mixpanel(PROJECT_TOKEN, consumer=AsyncBufferedConsumer())

    if settings.DEBUG:
        # To make everything work while testing.
        logger.warn("Mixpanel: PROJECT_TOKEN not found. Continuing with Mock()...")
        return Mock()

    raise ImproperlyConfigured("Must set 'MIXPANEL_PROJECT_TOKEN' in environment variable or provide "
                               "'PROJECT_TOKEN' while calling get_mixpanel_client().")
