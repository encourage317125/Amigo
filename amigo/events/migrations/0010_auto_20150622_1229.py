# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# Third Party Stuff
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0009_event_venue_name'),
    ]

    operations = [
        migrations.RenameField(
            model_name='event',
            old_name='spots_available',
            new_name='total_spots',
        ),
    ]
