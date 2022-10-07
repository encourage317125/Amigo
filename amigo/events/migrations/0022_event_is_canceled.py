# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0021_invitetext'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='is_canceled',
            field=models.BooleanField(default=False, help_text='whether or not this event was canceled'),
        ),
    ]
