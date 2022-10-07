# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

# Third Party Stuff
from django.db.models import Q
from rest_framework import filters

# Amigo Stuff
from amigo.events.models import Event
from amigo.base.utils.urls import get_datetime_from_query_params

from .utils.variables import to_boolean


class OrderingFilter(filters.OrderingFilter):
    pass


class CanViewEventObjFilterBackend(filters.BaseFilterBackend):

    def filter_queryset(self, request, queryset, view):
        qs = queryset

        if request.user.is_authenticated():
            # rethink this implementation, should include the events that i'm
            # invited to?
            qs = Event.objects.filter(owner=request.user)

        else:
            qs = queryset.none()

        return qs.distinct()


class IsEventInviteeFilterBackend(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        if request.user.is_authenticated():
            queryset = queryset.filter(Q(invitees__phone_number=request.user.phone_number) |
                                       Q(owner=request.user))
        else:
            queryset = queryset.none()

        return queryset.distinct()


class EventDateFilterBackend(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):

        event_after = get_datetime_from_query_params(request, 'event_after')
        event_before = get_datetime_from_query_params(request, 'event_before')

        if event_after:
            queryset = queryset.filter(event_date__gt=event_after)

        if event_before:
            queryset = queryset.filter(event_date__lt=event_before)

        return queryset.distinct()


class IamOwnerFilterBackend(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        try:
            querystring_value = to_boolean(request.QUERY_PARAMS.get('i_am_owner', None))
        except TypeError:
            pass

        if querystring_value is True:
            queryset = queryset.filter(owner=request.user)
        elif querystring_value is False:
            queryset = queryset.exclude(owner=request.user)

        return queryset.distinct()
