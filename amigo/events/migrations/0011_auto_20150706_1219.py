# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# Third Party Stuff
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0010_auto_20150622_1229'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='event',
            options={'permissions': (('view_event', 'Can view event'),), 'verbose_name_plural': 'events', 'verbose_name': 'event', 'ordering': ['-created']},
        ),
    ]
