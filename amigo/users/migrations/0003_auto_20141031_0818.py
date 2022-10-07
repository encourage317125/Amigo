# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# Third Party Stuff
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20141010_1110'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='notify_invite_change',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='user',
            name='notify_invite_rsvp',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='user',
            name='notify_new_invite',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
    ]
