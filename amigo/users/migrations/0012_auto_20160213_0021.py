# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0011_user_is_app_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='first_interaction',
            field=models.DateTimeField(default=None, null=True, verbose_name='first_interaction'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='user',
            name='is_app_user',
            field=models.BooleanField(default=False, verbose_name='app_user'),
            preserve_default=True,
        ),
    ]
