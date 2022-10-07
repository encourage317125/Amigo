# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# Third Party Stuff
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20141105_1028'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='notify_event_change',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
    ]
