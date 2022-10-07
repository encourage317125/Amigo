# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# Third Party Stuff
import django.utils.timezone
import django_extensions.db.fields
import jsonfield.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0006_auto_20150608_1446'),
    ]

    operations = [
        migrations.CreateModel(
            name='SampleRSVPReply',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('created', django_extensions.db.fields.CreationDateTimeField(default=django.utils.timezone.now, blank=True, verbose_name='created', editable=False)),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(default=django.utils.timezone.now, blank=True, verbose_name='modified', editable=False)),
                ('text', models.CharField(unique=True, max_length=60)),
                ('type', models.CharField(max_length=10, choices=[(b'accept', b'accept'), (b'reject', b'reject')])),
            ],
            options={
                'verbose_name': 'sample RSVP message',
                'verbose_name_plural': 'sample RSVP messages',
                'ordering': ['type', 'text'],
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='event',
            name='location',
            field=jsonfield.fields.JSONField(default={}, blank=True),
            preserve_default=True,
        ),
    ]
