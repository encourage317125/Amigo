# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0016_auto_20160202_0133'),
    ]

    operations = [
        migrations.AddField(
            model_name='invitation',
            name='invitee_current_status',
            field=models.IntegerField(default=0, help_text='This allows querying invitation                                                             status based on user action for analytics.', choices=[(0, 'App User'), (1, 'Passive User'), (2, 'New User')]),
        ),
        migrations.AlterField(
            model_name='invitation',
            name='invited_by',
            field=models.ForeignKey(related_name='ihaveinvited', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]
