# -*- coding: utf-8 -*-
# Standard Library
from collections import namedtuple
from datetime import timedelta

# Third Party Stuff
from django.conf import settings
from django.utils.timezone import now
from rest_framework.decorators import detail_route, list_route

# Amigo Stuff
from amigo.base import exceptions as exc
from amigo.base import filters, response
from amigo.base.api.viewsets import ModelCrudViewSet
from amigo.base.utils.urls import get_datetime_from_query_params

from . import services as events_services
from . import models, serializers


def parse_timeline_queryparams(request):
    event_type = request.query_params.get('type', '').lower()
    try:
        exclude_ids = request.query_params['exclude_ids'].strip()
        exclude_ids = exclude_ids.split('|')
    except KeyError:
        exclude_ids = None

    try:
        page_size = int(request.query_params['per_page'])
    except (ValueError, KeyError):
        page_size = settings.REST_FRAMEWORK['PAGE_SIZE']

    if event_type not in ['sent', 'received']:
        raise exc.BadRequest("Must provide 'type' query params with either 'sent' or 'received' value.")

    cursor_time = get_datetime_from_query_params(request, 'cursor')

    QueryParams = namedtuple('QueryDict', 'type page_size cursor_time exclude_ids')
    return QueryParams(event_type, page_size, cursor_time, exclude_ids)


class EventsViewSet(ModelCrudViewSet):
    serializer_class = serializers.EventDetailSerializer
    list_serializer_class = serializers.EventListSerializer
    queryset = models.Event.objects.all()
    filter_backends = (filters.IsEventInviteeFilterBackend, filters.EventDateFilterBackend,
                       filters.IamOwnerFilterBackend)

    @detail_route(methods=["POST"])
    def accept(self, request, pk=None):
        serializer = serializers.EventRSVPSerializer(data=request.data)
        if serializer.is_valid():
            event = self.get_object()
            events_services.mark_user_as_attending(event=event, user=request.user, **serializer.validated_data)
            return self.retrieve(request, pk)
        else:
            return response.BadRequest(serializer.errors)

    @detail_route(methods=["POST"])
    def reject(self, request, pk=None):
        serializer = serializers.EventRSVPSerializer(data=request.data)
        if serializer.is_valid():
            event = self.get_object()
            events_services.mark_user_as_unattending(event=event, user=request.user, **serializer.validated_data)
            return self.retrieve(request, pk)
        else:
            return response.BadRequest(serializer.errors)

    @detail_route(methods=['PUT'])
    def cancel_event(self, request, pk=None):
        serializer = serializers.EventCancelSerializer(data=request.data)
        # owner = request.user
        # event = Event.objects.get(pk=pk)
        # if serializer.is_valid():
        event = self.get_object()
        serializer.cancel(event, request.user)
        return response.NoContent()

    @list_route(methods=["GET"])
    def sample_rsvp_replies(self, request):
        qs = models.SampleRSVPReply.objects.all()
        serializer = serializers.EventSampleRSVPReplySerializer(qs, many=True)
        return response.Ok(serializer.data)

    @list_route(methods=["GET"])
    def stats(self, request):
        unresponded_invite_count = events_services.get_unresponded_invitations(request.user).count()
        return response.Ok({
            'unresponded_invite_count': unresponded_invite_count
        })

    @list_route(methods=["GET"])
    def timeline(self, request):
        query_params = parse_timeline_queryparams(request)
        upcoming_events_time = now() - timedelta(hours=2)

        # default to upcoming events, sorted in ascending
        qs = models.Event.objects.all()

        if query_params.type == 'sent':
            qs = qs.filter(owner=request.user)
        elif query_params.type == 'received':
            qs = qs.exclude(owner=request.user).filter(invitees__phone_number=request.user.phone_number)

        if query_params.exclude_ids:
            qs = qs.exclude(id__in=query_params.exclude_ids)

        # if cusor time is provided for expired event, return past event and be
        # done with it.
        expired_qs = qs.expired().order_by('-event_date', '-created')
        if query_params.cursor_time and query_params.cursor_time < upcoming_events_time:
            expired_qs = expired_qs.filter(event_date__lte=query_params.cursor_time)
            expired_qs = expired_qs[:query_params.page_size]
            expired_event_data = self.list_serializer_class(expired_qs, many=True, context={'request': request}).data
            return response.Ok(expired_event_data)

        # fetch upcoming events.
        upcoming_qs = qs.upcoming().order_by('event_date', '-created')
        if query_params.cursor_time and query_params.cursor_time > upcoming_events_time:
            upcoming_qs = upcoming_qs.filter(event_date__gt=query_params.cursor_time)

        upcoming_qs = upcoming_qs[:query_params.page_size]
        upcoming_event_data = self.list_serializer_class(upcoming_qs, many=True, context={'request': request}).data

        # if upcoming event data < page_size, fetch the expired events
        more_data_needed = query_params.page_size - len(upcoming_event_data)
        expired_event_data = []
        if more_data_needed > 0:
            expired_qs = expired_qs[:more_data_needed]
            expired_event_data = self.list_serializer_class(expired_qs,
                                                            many=True, context={'request': request}).data

        data = upcoming_event_data + expired_event_data
        return response.Ok(data)

    @list_route(methods=["GET"])
    def feedall(self, request):
        query_params = parse_timeline_queryparams(request)
        upcoming_events_time = now() - timedelta(hours=2)

        # default to upcoming events, not canceled, sorted in ascending
        qs = models.Event.objects.filter(is_canceled=False)

        # first we get sent events
        qs_sent = qs.filter(owner=request.user)
        qs_received = qs.exclude(owner=request.user).filter(invitees__phone_number=request.user.phone_number)

        if query_params.exclude_ids:
            qs_sent = qs.exclude(id__in=query_params.exclude_ids)

        # if cusor time is provided for expired event, return past event and be
        # done with it.
        expired_qs_sent = qs_sent.expired().order_by('-event_date', '-created')
        expired_qs_received = qs_received.expired().order_by('-event_date', '-created')

        if query_params.cursor_time and query_params.cursor_time < upcoming_events_time:
            expired_qs_sent = expired_qs_sent.filter(event_date__lte=query_params.cursor_time)
            expired_qs_sent = expired_qs_sent[:query_params.page_size]

            expired_qs_received = expired_qs_received.filter(event_date__lte=query_params.cursor_time)
            expired_qs_received = expired_qs_received[:query_params.page_size]

            expired_event_data = self.list_serializer_class(
                expired_qs_sent,
                many=True,
                context={'request': request}
            ).data + \
                self.list_serializer_class(
                    expired_qs_received,
                    many=True,
                    context={'request': request}).data
            return response.Ok(expired_event_data)

        # fetch upcoming events sent.
        upcoming_qs_sent = qs_sent.upcoming().order_by('event_date', '-created')
        if query_params.cursor_time and query_params.cursor_time > upcoming_events_time:
            upcoming_qs_sent = upcoming_qs_sent.filter(event_date__gt=query_params.cursor_time)

        upcoming_qs_sent = upcoming_qs_sent[:query_params.page_size]
        upcoming_sent_event_data = self.list_serializer_class(upcoming_qs_sent,
                                                              many=True, context={'request': request}).data

        # fetch upcoming events received
        upcoming_qs_received = qs_received.upcoming().order_by('event_date', '-created')
        if query_params.cursor_time and query_params.cursor_time > upcoming_events_time:
            upcoming_qs_received = upcoming_qs_received.filter(event_date__gt=query_params.cursor_time)

        upcoming_qs_received = upcoming_qs_received[:query_params.page_size]
        upcoming_received_event_data = self.list_serializer_class(upcoming_qs_received,
                                                                  many=True, context={'request': request}).data

        # if upcoming event data < page_size, fetch the expired events
        # fetch expired sent events
        more_data_needed = query_params.page_size - len(upcoming_sent_event_data)
        expired_sent_event_data = []
        if more_data_needed > 0:
            expired_qs_sent = expired_qs_sent[:more_data_needed]
            expired_sent_event_data = self.list_serializer_class(expired_qs_sent,
                                                                 many=True, context={'request': request}).data

        data_sent = upcoming_sent_event_data + expired_sent_event_data

        # fetch expired received events
        more_data_needed = query_params.page_size - len(upcoming_received_event_data)
        expired_received_event_data = []
        if more_data_needed > 0:
            expired_qs_received = expired_qs_received[:more_data_needed]
            expired_received_event_data = self.list_serializer_class(expired_qs_received,
                                                                     many=True, context={'request': request}).data

        data_received = upcoming_received_event_data + expired_received_event_data

        data = data_sent + data_received

        return response.Ok(data)
