# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

# Third Party Stuff
from django.conf.urls import patterns, url
from django.views.generic import TemplateView
from . import views
from django.conf import settings
from django.conf.urls.static import static
'''
Pages App Routing.

Handles the top level site pages. You would probably like to add the pages like
homepage, about, terms and conditions, etc. in this app.
'''


# Top Level Pages
# ==============================================================================
urlpatterns = patterns('',
    url(r'^$',  # noqa
        TemplateView.as_view(template_name='pages/index.html'), name="index"),
    url(r'^terms-of-use/$',
        TemplateView.as_view(template_name='pages/terms.html'), name="terms"),
    url(r'^privacy/$',
        TemplateView.as_view(template_name='pages/privacy.html'), name="privacy"),
    url(r'^use-license/$',
        TemplateView.as_view(template_name='pages/use_license.html'), name="use_license"),
    url(r'^faq/$',
        TemplateView.as_view(template_name='pages/faq.html'), name="faq"),
    url(r'^invitation/$', views.invitation, name="invitation"),
    url(r'^invitation/calendar/$', views.calendar, name="invitation_calendar"),
    url(r'^send_email/$', views.send_email, name="send_email"),
    url(r'^send_sms/$', views.send_sms, name="send_sms"),
    url(r'^subscribe_mailchimp/$', views.subscribe_mailchimp, name="subscribe_mailchimp"),
) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
