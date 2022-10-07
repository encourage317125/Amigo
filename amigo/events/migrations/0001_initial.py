# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# Third Party Stuff
import django.utils.timezone
import django_extensions.db.fields
from django.conf import settings
from django.db import migrations, models

# Amigo Stuff
import amigo.base.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(default=django.utils.timezone.now, verbose_name='created', editable=False, blank=True)),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(default=django.utils.timezone.now, verbose_name='modified', editable=False, blank=True)),
                ('title', models.CharField(max_length=250, verbose_name='title')),
                ('event_date', models.DateTimeField(verbose_name='created date')),
                ('spots_available', models.PositiveIntegerField(default=0, verbose_name='max. spots available')),
                ('spots_filled', models.PositiveIntegerField(default=0, verbose_name='spots filled having no users', blank=True)),
            ],
            options={
                'ordering': ['created'],
                'verbose_name': 'event',
                'verbose_name_plural': 'events',
                'permissions': (('view_event', 'Can view event'),),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Invitation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_owner', models.BooleanField(default=False)),
                ('phone_number', amigo.base.fields.PhoneNumberField(default=None, max_length=128, null=True, verbose_name='phone number', blank=True)),
                ('created', models.DateTimeField(default=django.utils.timezone.now, verbose_name='created at')),
                ('has_accepted_invite', models.BooleanField(default=False)),
                ('event', models.ForeignKey(related_name=b'invitations', to='events.Event')),
                ('invited_by', models.ForeignKey(related_name=b'ihaveinvited+', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('user', models.ForeignKey(related_name=b'invitations', default=None, blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ['event', 'user__full_name', 'user__phone_number'],
                'verbose_name': 'invitation',
                'verbose_name_plural': 'invitations',
                'permissions': (('view_invitation', 'Can view invitation'),),
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='invitation',
            unique_together=set([('user', 'event')]),
        ),
        migrations.AddField(
            model_name='event',
            name='attendees',
            field=models.ManyToManyField(related_name=b'events', verbose_name='attendees', through='events.Invitation', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='event',
            name='owner',
            field=models.ForeignKey(related_name=b'owned_events', verbose_name='owner', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
