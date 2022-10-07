# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import jsonfield.fields
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0019_sample_events'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='sampleevent',
            options={'verbose_name': 'Sample Event', 'verbose_name_plural': 'Sample Events', 'permissions': (('view_event', 'Can view event'),)},
        ),
        migrations.AlterField(
            model_name='sampleevent',
            name='address',
            field=models.TextField(default='', blank=True),
        ),
        migrations.AlterField(
            model_name='sampleevent',
            name='created',
            field=django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created'),
        ),
        migrations.AlterField(
            model_name='sampleevent',
            name='event_date',
            field=models.DateTimeField(verbose_name='Event Date'),
        ),
        migrations.AlterField(
            model_name='sampleevent',
            name='location',
            field=jsonfield.fields.JSONField(default={}, blank=True),
        ),
        migrations.AlterField(
            model_name='sampleevent',
            name='modified',
            field=django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified'),
        ),
        migrations.AlterField(
            model_name='sampleevent',
            name='venue_name',
            field=models.CharField(max_length=200, verbose_name='Venue Name', blank=True),
        ),
    ]
