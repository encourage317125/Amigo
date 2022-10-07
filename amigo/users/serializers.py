# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

# Third Party Stuff
from rest_framework import serializers
from facebook import GraphAPI
from django.core.files import File
import requests
import shutil

# Amigo Stuff
from amigo.base.serializers import PhoneNumberListField

from . import models, services


class UserSerializer(serializers.ModelSerializer):
    photo = serializers.SerializerMethodField()
    big_photo = serializers.SerializerMethodField()

    class Meta:
        model = models.User
        fields = ("id", "phone_number", "full_name", "email",
                  "is_active", "notify_new_invite", "notify_invite_rsvp",
                  "photo", "big_photo", "notify_contact_joined", "notify_event_full",
                  "notify_upcoming_event", )
        read_only_fields = ("id", "is_active", "phone_number")

    def get_photo(self, user):
        return services.get_photo_or_none(user)

    def get_big_photo(self, user):
        return services.get_big_photo_or_none(user)


class UserPhotoSerializer(serializers.ModelSerializer):
    photo = serializers.ImageField(required=True, allow_empty_file=False)

    class Meta:
        model = models.User
        fields = ("photo", )
        required_fieds = ("photo", )


class ContactUserSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        fields = ('id', 'full_name', 'phone_number', 'photo', 'big_photo')


class UserFbTokenSerializer(UserSerializer):
    fb_token = serializers.CharField(required=True)

    def update(self, user, validated_data):
        fb_token = validated_data.get('fb_token', user.fb_token)
        graph = GraphAPI(access_token=fb_token, version='2.5')
        fb_profile = graph.get_object('me', fields='first_name,last_name,email,picture.height(961)')
        user.fb_token = fb_token
        user.email = fb_profile['email']
        user.full_name = '{0} {1}'.format(fb_profile['first_name'], fb_profile['last_name'])
        user.photo_uri = fb_profile['picture']['data']['url']

        # Download FB picture if user does not have a photo yet
        if not user.photo:
            resp = requests.get(user.photo_uri, stream=True)
            if resp.status_code == 200:
                with open('/tmp/fb_picture.jpg', 'wb') as tmp_img:
                    resp.raw.decode_content = True
                    shutil.copyfileobj(resp.raw, tmp_img)
            user.photo = File(open('/tmp/fb_picture.jpg'), 'r')
        user.save()

        return user

    class Meta(UserSerializer.Meta):
        fields = ('id', 'full_name', 'phone_number', 'fb_token')


class FavoriteContactSerializer(serializers.ModelSerializer):
    user = ContactUserSerializer()
    is_favorite = serializers.SerializerMethodField()

    class Meta:
        model = models.FavoriteContact
        fields = ('id', 'phone_number', 'user', 'is_favorite')

    def get_is_favorite(self, obj):
        '''
        This is done here only to serializer as per the requirement by iOS
        app. All the objects passed to this serializer will always have
        is_favorite = True
        '''
        return True


class AddDeleteFavoriteBulkSerializer(serializers.Serializer):
    phone_numbers = PhoneNumberListField(required=True)

    class Meta:
        fields = ['phone_numbers']


class ContactSerializer(serializers.Serializer):
    phone_number = serializers.SerializerMethodField()
    user = serializers.SerializerMethodField()

    class Meta:
        fields = ('phone_number', 'user', )

    def get_phone_number(self, user):
        return user.phone_number

    def get_user(self, user):
        return ContactUserSerializer(user).data
