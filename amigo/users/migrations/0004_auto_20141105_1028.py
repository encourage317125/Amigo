# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# Third Party Stuff
import uuid_upload_path.storage
import versatileimagefield.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20141031_0818'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='photo',
            field=versatileimagefield.fields.VersatileImageField(verbose_name='photo', blank=True, upload_to=uuid_upload_path.storage.upload_to, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='user',
            name='photo_poi',
            field=versatileimagefield.fields.PPOIField(verbose_name="photo's Point of Interest", default=b'0.5x0.5', max_length=20),
            preserve_default=True,
        ),
    ]
