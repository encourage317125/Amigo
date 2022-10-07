# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# Third Party Stuff
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0007_auto_20150611_1808'),
    ]

    operations = [
        migrations.AddField(
            model_name='invitation',
            name='rsvp_time',
            field=models.DateTimeField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
