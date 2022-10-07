# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

# Third Party Stuff
from rest_framework import permissions as drf_permissions


class AllowAny(drf_permissions.AllowAny):
    """
    Allow any access.
    This isn't strictly required, since you could use an empty
    permission_classes list, but it's useful because it makes the intention
    more explicit.
    """
    pass


class IsAuthenticated(drf_permissions.IsAuthenticated):
    """
    Allows access only to authenticated users.
    """
    pass
