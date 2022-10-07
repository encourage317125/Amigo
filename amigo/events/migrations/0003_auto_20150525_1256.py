# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# Third Party Stuff
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0002_invitation_has_seen'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invitation',
            name='has_accepted_invite',
            field=models.NullBooleanField(default=None),
            preserve_default=True,
        ),
    ]
