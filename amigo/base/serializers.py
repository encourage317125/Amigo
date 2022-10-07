# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

# Third Party Stuff
from rest_framework import serializers


class ModelSerializer(serializers.ModelSerializer):

    def perform_validation(self, attrs):
        for attr in attrs:
            field = self.fields.get(attr, None)
            if field:
                field.required = True
        return super(ModelSerializer, self).perform_validation(attrs)


class InviteeSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=15)
    name = serializers.CharField(max_length=80)
    photo = serializers.URLField()


class PhoneNumberListField(serializers.ListField):
    phone = serializers.CharField(max_length=15)


class InviteesSerializer(serializers.Serializer):
    invitees = serializers.ListField(child=InviteeSerializer())
