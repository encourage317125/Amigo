# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# Third Party Stuff
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_user_notify_event_change'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='notify_contact_joined',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
    ]
