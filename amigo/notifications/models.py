# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import shortuuid

from django.db import models

from amigo.events.models import Event
from amigo.users.models import User


class EventToken(models.Model):
    token = models.CharField(max_length=255, db_index=True)
    user = models.ForeignKey(User, null=False, blank=False)
    used_at = models.DateTimeField(null=True, blank=True)
    event = models.ForeignKey(Event)

    class Meta:
        app_label = 'notifications'

    def save_token(self):
        self.token = shortuuid.ShortUUID().random(length=5)
        super(EventToken, self).save()
