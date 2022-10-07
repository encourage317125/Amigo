# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# Third Party Stuff
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='invitation',
            name='has_seen',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
