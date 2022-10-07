# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

# Third Party Stuff
from rest_framework import serializers


class AppleDeviceSerializer(serializers.Serializer):
    token = serializers.CharField(max_length=255, required=True)
