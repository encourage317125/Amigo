# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# Third Party Stuff
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0008_invitation_rsvp_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='venue_name',
            field=models.CharField(blank=True, verbose_name='venue name', max_length=100),
            preserve_default=True,
        ),
    ]
