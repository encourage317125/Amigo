# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from datetime import datetime
import random

# Third Party Stuff
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from rest_framework import status
from rest_framework.decorators import list_route
from rest_framework.response import Response
from django.contrib.auth import get_user_model

# Amigo Stuff
from amigo.analytics import services as analytics_services
from amigo.base import exceptions as exc
from amigo.base.api import viewsets
from amigo.base.api.permissions import AllowAny, IsAuthenticated
from amigo.users.serializers import UserSerializer
from amigo.users.services import get_or_make_inactive_user
from amigo.users.models import User
from amigo.events.models import Event, SampleEvent, Invitation

from . import services
from .serializers import PinVerificationSerializer, PublicRegisterSerializer
from .services import make_auth_response_data


WEEKDAY_IDX = {'Sun': 0,
               'Mon': 1,
               'Tue': 2,
               'Wed': 3,
               'Thu': 4,
               'Fri': 5,
               'Sat': 6}


class AuthViewSet(viewsets.ViewSet):
    """
    Authorization resources.

    ## Login

    `POST` `/auth`

    **Parameters**

    - `phone_number` - Standard phone number, must include (+)

    ## Register

    `POST` `/auth/register`

    * **Note:** This endpoint required authorization.*

    **Parameters**

    - `full_name` - min. 2 chars and max. 256 characters
    - `email` - valid email address, max length 256 chars
    """
    permission_classes = [AllowAny, ]

    def _login(self, request):
        phone_number = request.data.get('phone_number', None)

        if not phone_number:
            raise exc.BadRequest(_("Phone Number is not provided."))

        user = get_or_make_inactive_user(phone_number=phone_number, app_user=True)
        data = UserSerializer(user).data

        return Response(data, status=status.HTTP_204_NO_CONTENT)

    def _public_register(self, request):
        if not settings.PUBLIC_REGISTER_ENABLED:
            raise exc.BadRequest(_("Public register is disabled."))

        serializer = PublicRegisterSerializer(request.user, data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.save()
        analytics_services.track_user_registration(user)
        services.send_new_contact_joined_notification(user)

        data = make_auth_response_data(user)
        return Response(data, status=status.HTTP_200_OK)

    # Login view: POST /api/auth
    def create(self, request, **kwargs):
        """
        Endpoint to login.
        """
        return self._login(request)

    def __allocate_sample_received_events(self, user):
        """Allocate 3 sample received events for this newly activated user"""
        sample_events = list(SampleEvent.objects.filter(type='received'))

        for _i in range(0, 1):
            random.shuffle(sample_events)
            sample_evt = sample_events.pop()
            evt_owner = User.objects.filter(full_name='Amigo Team').first()
            sample_evt = Event(title=sample_evt.title,
                               owner=evt_owner,
                               address=sample_evt.address,
                               event_date=sample_evt.event_date,
                               venue_name=sample_evt.venue_name)
            sample_evt.save()

            """
            invitees_list = sample_evt[4].split(',')
            for invitee_name in invitees_list:
                invitee = User.objects.filter(full_name=invitee_name).first()
                print invitee
                if invitee:
                    invitation = Invitation(event=sample_evt,
                                            user=invitee,
                                            invited_by=evt_owner)
                    invitation.save()

            myself = User.objects.filter(phone_number=user.phone_number).first()
            """
            invitation = Invitation(event=sample_evt,
                                    user=user,
                                    invited_by=evt_owner)
            invitation.save()

    def __allocate_sample_sent_events(self, user):
        """Allocate 3 sample sent events for this newly activated user"""
        sample_events = list(SampleEvent.objects.filter(type='sent'))

        for _i in range(0, 1):
            random.shuffle(sample_events)
            sample_evt = sample_events.pop()
            sample_evt = Event(title=sample_evt.title,
                               owner=user,
                               address=sample_evt.address,
                               event_date=sample_evt.event_date,
                               venue_name=sample_evt.venue_name)
            sample_evt.save()

    @list_route(methods=["POST"])
    def verify_pin(self, request):
        serializer = PinVerificationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # The user is in the serializer as "phone_number"
        user = serializer.validated_data['phone_number']

        # Update user password with a random one
        user.set_password(get_user_model().objects.make_random_password())

        # tracks user's first active interaction with app
        if user.first_interaction is None:
            user.first_interaction = datetime.now()
            self.__allocate_sample_received_events(user)
            self.__allocate_sample_sent_events(user)

        user.is_active = True  # If valid pin was provided, active this user
        user.is_app_user = True
        data = make_auth_response_data(user)
        user.save()

        return Response(data, status=status.HTTP_200_OK)

    # Register view: /api/auth/register
    @list_route(permission_classes=[IsAuthenticated], methods=["POST"])
    def register(self, request, **kwargs):
        return self._public_register(request)
