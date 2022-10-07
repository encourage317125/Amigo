# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

# Third Party Stuff
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from rest_framework import serializers


class BaseRegisterSerializer(serializers.Serializer):
    full_name = serializers.CharField(max_length=256)
    email = serializers.EmailField(max_length=255)


class PublicRegisterSerializer(BaseRegisterSerializer,
                               serializers.ModelSerializer):
    is_active = serializers.HiddenField(default=True)

    class Meta:
        fields = ('full_name', 'email', 'is_active')
        model = get_user_model()


class PinVerificationSerializer(serializers.Serializer):
    phone_number = serializers.SlugRelatedField(
        slug_field='phone_number',
        queryset=get_user_model().objects.all()
    )
    pin = serializers.CharField(max_length=settings.SMS_VALIDATION_LENGTH)

    def validate(self, data):
        data = super(PinVerificationSerializer, self).validate(data)

        # Do this here only for testing purposes
        if settings.DEBUG and data['pin'] == '1111':
            return data

        # phone number is a phone_number model
        if not check_password(data['pin'], data['phone_number'].password):
            raise serializers.ValidationError("Pin is incorrect.")

        return data
