# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_auto_20150731_1357'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_app_user',
            field=models.BooleanField(default=True, verbose_name='app_user'),
            preserve_default=True,
        ),
    ]
