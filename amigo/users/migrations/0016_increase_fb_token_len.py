# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0015_user_photo_uri'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='fb_token',
            field=models.CharField(max_length=512, null=True, verbose_name='facebook access token', blank=True),
        ),
    ]
