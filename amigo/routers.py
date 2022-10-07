# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
'''This urls.py is for all API related URLs.

URL Naming Pattern (lowercased & underscored)
<app_name>_<model_name> or
<app_name>_<specific_action>

For base name use:
<app_name>
'''
# Third Party Stuff
from rest_framework import routers

# Amigo Stuff
from amigo.auth.api import AuthViewSet
from amigo.events.api import EventsViewSet
from amigo.notifications.api import NotificationsViewSet
from amigo.users.api import UsersViewSet

router = routers.DefaultRouter(trailing_slash=False)

# amigo.users
# -----------------------------------------------------------------------------
router.register(r"users", UsersViewSet, base_name="users")
router.register(r"auth", AuthViewSet, base_name="auth")
router.register(r"notifications", NotificationsViewSet, base_name="notifications")

# amigo.events
# -----------------------------------------------------------------------------
router.register(r"events", EventsViewSet, base_name="events")
