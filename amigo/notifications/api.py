# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

# Third Party Stuff
from rest_framework.decorators import list_route

# Amigo Stuff
# -*- coding: utf-8 -*-
# from django.utils.translation import ugettext_lazy as _
from amigo.base import response
from amigo.base.api import viewsets

from . import serializers
from .services import deregister_apple_device, register_apple_device


class NotificationsViewSet(viewsets.ViewSet):

    @list_route(methods=["POST"])
    def add_ios_device(self, request):
        serializer = serializers.AppleDeviceSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        device = register_apple_device(request.user, **serializer.validated_data)
        return response.Ok({'token': device.token,
                            'user_id': device.user.id})

    @list_route(methods=["POST"])
    def remove_ios_device(self, request):
        serializer = serializers.AppleDeviceSerializer(data=request.DATA)
        serializer.is_valid(raise_exception=True)

        token = serializer.validated_data['token']
        device = deregister_apple_device(request.user, token)
        if device:
            return response.Ok({'token': device.token,
                                'user_id': device.user.id,
                                'success': True})
        else:
            return response.Ok({'success': False,
                                'reason': "device is not registered for this user."})
