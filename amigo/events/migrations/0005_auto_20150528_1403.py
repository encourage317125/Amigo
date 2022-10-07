# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# Third Party Stuff
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0004_merge'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='is_time_specified',
            field=models.BooleanField(help_text=b'whether "event_date" contains a specific time of day.', default=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='event',
            name='event_date',
            field=models.DateTimeField(verbose_name='event date'),
            preserve_default=True,
        ),
    ]
