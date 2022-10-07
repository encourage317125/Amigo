# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# Third Party Stuff
import django_extensions.db.fields.json
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0005_auto_20150528_1403'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='address',
            field=models.TextField(default=b''),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='event',
            name='location',
            field=django_extensions.db.fields.json.JSONField(blank=True, null=True),
            preserve_default=True,
        ),
    ]
