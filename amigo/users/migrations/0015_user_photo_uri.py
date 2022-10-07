# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0014_user_fb_token'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='photo_uri',
            field=models.CharField(max_length=4000, null=True, verbose_name='photo uri', blank=True),
        ),
    ]
