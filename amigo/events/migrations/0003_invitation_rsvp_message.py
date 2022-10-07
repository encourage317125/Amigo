# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# Third Party Stuff
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0002_invitation_has_seen'),
    ]

    operations = [
        migrations.AddField(
            model_name='invitation',
            name='rsvp_message',
            field=models.CharField(null=True, blank=True, max_length=60, help_text=b'message sent while reponding to this invitation.'),
            preserve_default=True,
        ),
    ]
