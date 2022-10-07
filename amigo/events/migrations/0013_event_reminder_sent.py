# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# Third Party Stuff
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0012_auto_20150713_1007'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='reminder_sent',
            field=models.BooleanField(help_text='whether upcoming event reminder sent or not.', default=False),
            preserve_default=True,
        ),
    ]
