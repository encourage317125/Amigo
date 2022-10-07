# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# Third Party Stuff
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_auto_20150714_1407'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='notify_event_full',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='user',
            name='notify_upcoming_event',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
    ]
