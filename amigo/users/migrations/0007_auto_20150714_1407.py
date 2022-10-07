# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# Third Party Stuff
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_user_notify_contact_joined'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='notify_event_change',
        ),
        migrations.RemoveField(
            model_name='user',
            name='notify_invite_change',
        ),
    ]
