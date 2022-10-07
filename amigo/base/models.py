# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

# Third Party Stuff
from django.db import models
from django.utils.translation import ugettext_lazy as _
from uuid_upload_path import upload_to
from versatileimagefield.fields import VersatileImageField, PPOIField


class PhotoMixin(models.Model):

    photo = VersatileImageField(upload_to=upload_to, blank=True, null=True, ppoi_field='photo_poi',
                                verbose_name=_("photo"))
    photo_poi = PPOIField(verbose_name=_("photo's Point of Interest"))  # point of interest
    photo_uri = models.CharField(_('photo uri'), max_length=4000, blank=True, null=True)

    class Meta:
        verbose_name = 'Profile_Picture'
        verbose_name_plural = 'Profile_Pictures'
        abstract = True
