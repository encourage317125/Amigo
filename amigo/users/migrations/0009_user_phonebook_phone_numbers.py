# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# Third Party Stuff
import jsonfield.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_auto_20150714_1455'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='phonebook_phone_numbers',
            field=jsonfield.fields.JSONField(default=[]),
            preserve_default=True,
        ),
    ]
