# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0013_auto_20160219_0015'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='fb_token',
            field=models.CharField(max_length=256, null=True, verbose_name='facebook access token', blank=True),
        ),
    ]
