# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# Third Party Stuff
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0011_auto_20150706_1219'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='address',
            field=models.TextField(blank=True, default=b''),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='event',
            name='total_spots',
            field=models.PositiveIntegerField(verbose_name='total spots', default=0),
            preserve_default=True,
        ),
    ]
