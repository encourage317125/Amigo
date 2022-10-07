# -*- coding: utf-8 -*-

# Third Party Stuff
from django.core.exceptions import ValidationError
from rest_framework import serializers

# Amigo Stuff
from amigo.base.serializers import ModelSerializer, PhoneNumberListField
from amigo.base.services import get_event_rsvp_message, is_event_attending, is_event_owner
from amigo.users.serializers import UserSerializer
from amigo.users.services import get_big_photo_or_none, get_faded_photo_or_none, get_photo_or_none

from . import models, services


class EventInviteeSerializer(ModelSerializer):
    id = serializers.SerializerMethodField()
    full_name = serializers.SerializerMethodField()
    phone_number = serializers.SerializerMethodField()
    is_attending = serializers.CharField(source='has_accepted_invite', required=False)
    is_active = serializers.SerializerMethodField()
    photo = serializers.SerializerMethodField()
    big_photo = serializers.SerializerMethodField()
    faded_photo = serializers.SerializerMethodField()

    class Meta:
        model = models.Invitation
        fields = ("id", "full_name", "phone_number", "is_attending", "is_active", "is_owner", "has_seen",
                  "photo", "big_photo", "faded_photo", "rsvp_message", "rsvp_time", "created",)

    def get_full_name(self, obj):
        return obj.user.get_full_name() if obj.user else ""

    def get_phone_number(self, obj):
        return obj.user.phone_number if obj.user else obj.phone_number

    def get_is_active(self, obj):
        return obj.user.is_active if obj.user else False

    def get_id(self, obj):
        return obj.user.id if obj.user else 0

    def get_email(self, obj):
        return obj.user.email if obj.user else ""

    def get_photo(self, obj):
        return get_photo_or_none(obj.user) if obj.user else None

    def get_big_photo(self, obj):
        return get_big_photo_or_none(obj.user) if obj.user else None

    def get_faded_photo(self, obj):
        return get_faded_photo_or_none(obj.user) if obj.user else None


class EventBaseSerializer(ModelSerializer):
    i_am_owner = serializers.SerializerMethodField()
    i_am_attending = serializers.SerializerMethodField()
    my_rsvp_message = serializers.SerializerMethodField()
    owner = UserSerializer(read_only=True)
    is_time_specified = serializers.BooleanField(required=False)

    class Meta:
        model = models.Event
        fields = ("id", "title", "event_date", "created", "modified", "owner",
                  "i_am_owner", "i_am_attending", "is_time_specified", "location",
                  "address", "venue_name", "my_rsvp_message",)
        read_only_fields = ("id", )

    def get_i_am_owner(self, obj):
        if "request" in self.context:
            return is_event_owner(self.context["request"].user, obj)
        return False

    def get_my_rsvp_message(self, obj):
        if "request" in self.context:
            return get_event_rsvp_message(self.context["request"].user, obj)
        return False

    def get_i_am_attending(self, obj):
        if "request" in self.context:
            return is_event_attending(self.context["request"].user, obj)
        return None

    def get_invitees(self, obj):
        qs = models.Invitation.objects.filter(event=obj)
        serializer = EventInviteeSerializer(qs, many=True)
        return serializer.data

    def update(self, instance, validated_data):
        try:
            return super(EventBaseSerializer, self).update(instance, validated_data)
        except ValidationError as e:
            raise serializers.ValidationError(e.message_dict)


class EventListSerializer(EventBaseSerializer):
    invitees = serializers.SerializerMethodField()

    class Meta(EventBaseSerializer.Meta):
        fields = EventBaseSerializer.Meta.fields + ("invitees", )


class EventDetailSerializer(EventBaseSerializer):
    """Serializer for event details."""
    invitees = serializers.SerializerMethodField()
    invite_phone_numbers = PhoneNumberListField(required=False, write_only=True)

    class Meta(EventBaseSerializer.Meta):
        fields = EventBaseSerializer.Meta.fields + ("invitees", "invite_phone_numbers",)

    def create(self, validated_data):
        # remove invite_phone_numbers and add owner
        invite_phone_numbers = validated_data.pop('invite_phone_numbers', None)

        validated_data['owner'] = self.context['request'].user

        instance = super(EventDetailSerializer, self).create(validated_data)

        if invite_phone_numbers:
            services.add_bulk_invitation_by_phone(event=instance,
                                                  invitees=invite_phone_numbers,
                                                  invited_by=validated_data['owner'])
        return instance

    def update(self, instance, validated_data):
        invite_phone_numbers = validated_data.pop('invite_phone_numbers', None)
        instance = super(EventDetailSerializer, self).update(instance, validated_data)
        if invite_phone_numbers:
            services.add_bulk_invitation_by_phone(event=instance,
                                                  invitees=invite_phone_numbers,
                                                  invited_by=instance.owner)
        return instance


class EventRSVPSerializer(serializers.Serializer):
    rsvp_message = serializers.CharField(max_length=60, required=False)


class EventSampleRSVPReplySerializer(ModelSerializer):

    class Meta:
        model = models.SampleRSVPReply
        fields = ("id", "text", "type",)


class EventCancelSerializer(EventBaseSerializer):

    class Meta(EventBaseSerializer.Meta):
        fields = EventBaseSerializer.Meta.fields + ("is_canceled",)

    def validate(self, data):
        return data

    def cancel(self, event, user):
        # super(EventBaseSerializer, self).i_am_owner
        # if "request" in self.context:
        if event.owner == user:
            # owner = self.context["request"].user
            event.is_canceled = True
            event.save()
            return event
        else:
            raise serializers.ValidationError("You are not the owner of this event and cannot cancel it")
