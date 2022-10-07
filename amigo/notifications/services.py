# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

# Standard Library
import logging
import os

# Third Party Stuff
from django.conf import settings
from django.utils.encoding import smart_str
# from django_twilio_sms.utils import send_sms as twilio_send_sms
from twilio.rest import TwilioRestClient
from twilio.rest.exceptions import TwilioRestException
from zeropush.models import PushDevice
from amigo.analytics.mixpanel_client import get_mixpanel_client

from .utils import notify_devices

log = logging.getLogger(__name__)


def register_apple_device(user, token):
    if token:
        mp = get_mixpanel_client()
        mp.people_union(user.id, {"$ios_devices": [token]})

    device = PushDevice.objects.filter(token=token).first()
    if device:
        device.user = user
        device.save()
        return device
    else:
        return PushDevice.objects.create(token=token, user=user)


def deregister_apple_device(user, token):
    device = PushDevice.objects.filter(token=token, user=user).first()
    if device:
        device.delete()
        return device
    else:
        return False


def send_bulk_sms(phone_numbers, body):
    '''TODO: make it async?'''
    return [send_sms(phone_number, body) for phone_number in phone_numbers]


def send_sms(to, body, request=None):
    '''Application level abstraction for sending sms.
    '''

    '''
    TODO: make it async?
    '''

    if os.environ['DEBUG'] == 'True':
        return True
    else:
        try:
            client = TwilioRestClient(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
            result = client.messages.create(to=to, from_="+12084030909", body=body)
            # result = twilio_send_sms(request=request, to_number=to, body=body)
            return result
        except TwilioRestException as e:
            # suppress and log invalid phone number exception
            if "not a valid phone number" in str(e) or "is not a mobile number" in str(e):
                log.warn("TwilioRestException: %s" % str(e))
            else:
                raise e


def send_push_notification(user, alert=None, sound='default', badge=None, info=None, expiry=None,
                           content_available=None, category=None):
    if getattr(settings, 'DISABLE_PUSH_NOTIFICATION', False):
        log.info("Sent to %s: %s" % (smart_str(user.get_full_name()), smart_str(alert)))
        return True

    return notify_devices(user.pushdevice_set.all(), alert=alert, sound=sound, badge=badge,
                          info=info, expiry=expiry, content_available=content_available,
                          category=category)


def send_bulk_push_notification(users, alert=None, sound='default', badge=None, info=None, expiry=None,
                                content_available=None, category=None):

    devices = [user.pushdevice_set.all() for user in users]

    # http://stackoverflow.com/a/952952
    merged_devices = [item for sublist in devices for item in sublist]

    if getattr(settings, 'DISABLE_PUSH_NOTIFICATION', False):
        log.info("Sent to %s: %s" % (merged_devices, smart_str(alert)))
        return True

    return notify_devices(merged_devices, alert=alert, sound=sound, badge=badge,
                          info=info, expiry=expiry, content_available=content_available,
                          category=category)
