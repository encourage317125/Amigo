# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0014_auto_20150730_1558'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='total_spots',
            field=models.PositiveIntegerField(default=1, verbose_name='total spots', validators=[django.core.validators.MinValueValidator(1)]),
            preserve_default=True,
        ),
    ]
