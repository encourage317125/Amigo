# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('events', '0013_event_reminder_sent'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='event',
            options={'verbose_name_plural': 'events', 'ordering': ['-event_date', 'title'], 'permissions': (('view_event', 'Can view event'),), 'verbose_name': 'event'},
        ),
        migrations.RemoveField(
            model_name='event',
            name='attendees',
        ),
        migrations.AddField(
            model_name='event',
            name='invitees',
            field=models.ManyToManyField(related_name='events', through='events.Invitation', to=settings.AUTH_USER_MODEL, verbose_name='invitees'),
            preserve_default=True,
        ),
    ]
