# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

# Third Party Stuff
from django.utils.translation import ugettext_lazy as _
from rest_framework.decorators import list_route
from facebook import GraphAPI, GraphAPIError

# Amigo Stuff
from amigo.base import exceptions as exc
from amigo.base import response
from amigo.base.api.viewsets import ModelCrudViewSet
from amigo.events.models import Invitation

from . import models, serializers, services


def parse_phone_numbers(request):
    if 'phone_numbers' not in request.data.keys():
        raise exc.BadRequest(_("phone_numbers parameter is missing"))

    phone_numbers = request.data['phone_numbers']
    if type(phone_numbers) is not list:
        raise exc.BadRequest(_("phone_numbers must be of type list"))

    return phone_numbers


class UsersViewSet(ModelCrudViewSet):
    serializer_class = serializers.UserSerializer
    queryset = models.User.objects.all()

    def create(self, *args, **kwargs):
        raise exc.NotSupported()

    @list_route(methods=["POST"])
    def change_avatar(self, request):
        """Change avatar to current logged user. """

        serializer = serializers.UserPhotoSerializer(instance=request.user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            user_data = serializers.UserSerializer(request.user).data
            return response.Ok(user_data)
        else:
            return response.BadRequest(serializer.errors)

    @list_route(methods=["POST"])
    def remove_avatar(self, request):
        """Remove the avatar of current logged user. """
        request.user.photo = None
        request.user.save(update_fields=["photo"])
        user_data = serializers.UserSerializer(request.user).data
        return response.Ok(user_data)

    @list_route(methods=["POST"])
    def from_phone_numbers(self, request):
        phone_numbers = parse_phone_numbers(request)
        users = models.User.objects.filter(phone_number__in=phone_numbers, is_active=True)
        data = serializers.ContactSerializer(users, many=True).data

        # Save phonebook numbers for future uses, this assumes that all the
        # phonebook contacts are sent everytime, this endpoint is called.
        request.user.phonebook_phone_numbers = phone_numbers
        request.user.save()
        return response.Ok(data)

    @list_route(methods=["GET"])
    def who_has_invited_me(self, request):
        i_am_invited_by = Invitation.objects.filter(user=request.user).values_list('invited_by')
        users = models.User.objects.filter(id__in=i_am_invited_by, is_active=True)
        data = serializers.UserSerializer(users, many=True).data
        return response.Ok(data)

    @list_route(methods=['GET', 'POST', 'PATCH', 'DELETE'])
    def favorite_contacts(self, request, pk=None):
        if request.method == 'GET':
            contacts = services.get_contacts_and_associated_user(owner=request.user)
            data = serializers.FavoriteContactSerializer(contacts, many=True).data
            return response.Ok(data)

        phone_numbers = parse_phone_numbers(request)

        if request.method == 'POST':
            services.add_favorite_in_bulk(request.user, phone_numbers)
            contacts = services.get_contacts_and_associated_user(owner=request.user)
            data = serializers.FavoriteContactSerializer(contacts, many=True).data
            return response.Ok(data)

        # allow `PATCH` here as iOS RestKit doesn't allow raw data in DELETE method
        if request.method == 'DELETE' or request.method == 'PATCH':
            models.FavoriteContact.objects.filter(owner=request.user, phone_number__in=phone_numbers).delete()
        return response.NoContent()

    @list_route(methods=["POST"])
    def register_fb_token(self, request):
        """Register facebook token to current logged user. """
        serializer = serializers.UserFbTokenSerializer(instance=request.user, data=request.data)
        if serializer.is_valid():
            try:
                serializer.save()
                user_data = serializers.UserSerializer(request.user).data
                return response.Ok(user_data)
            except GraphAPIError:
                return response.BadRequest("Invalid Facebook access token")
        else:
            return response.BadRequest(serializer.errors)

    @list_route(methods=["GET"])
    def fb_friends(self, request):
        """Retrieve facebook friends of the current logged user. """

        if request.user.fb_token:
            try:
                graph = GraphAPI(access_token=request.user.fb_token, version='2.5')
                friends = graph.get_connections(id='me', connection_name='friends')['data']
                return response.Ok(friends)
            except GraphAPIError:
                return response.BadRequest("Invalid Facebook access token")
        else:
            return response.BadRequest("No Facebook access token provided")
