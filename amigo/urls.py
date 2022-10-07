# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

# Third Party Stuff
from django.conf import settings
from django.conf.urls import include, patterns, url
from django.conf.urls.static import static
from django.contrib import admin

from .routers import router


handler500 = "amigo.base.api.views.server_error"

urlpatterns = patterns('',  # noqa

    # Timezone Detection
    url(r'^tz_detect/', include('tz_detect.urls')),

    # Rest API
    url(r'^api/', include(router.urls)),

    url(r'^grappelli/', include('grappelli.urls')),  # grappelli URLS
    url(r'^admin/', include(admin.site.urls)),

    # Twilio sms callback
    # see: https://github.com/theskumar/django-twilio-sms-2#quickstart
    url(r'^messaging/', include('django_twilio_sms.urls')),

    # These URLS provide the login/logout functions for the browseable API.
    url(r'^v1/auth-n/', include('rest_framework.urls', namespace='rest_framework')),

    # For perfomance reasons, put least specific url at bottom.
    url(r'^', include("amigo.pages.urls", namespace="pages")),

) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^400/$', 'django.views.defaults.bad_request'),  # noqa
        url(r'^403/$', 'django.views.defaults.permission_denied'),
        url(r'^404/$', 'django.views.defaults.page_not_found'),
        url(r'^500/$', 'amigo.base.api.views.server_error'),
    )
