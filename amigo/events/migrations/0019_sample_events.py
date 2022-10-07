# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# Amigo stuff
from amigo.users.models import User
from amigo.events.models import SampleEvent

# Third Party Stuff
import pytz
from datetime import datetime, timedelta
import django
from django.db import migrations, models
import django_extensions.db.fields.json
from django.conf import settings


WEEKDAY_IDX = {'Sun': 0,
               'Mon': 1,
               'Tue': 2,
               'Wed': 3,
               'Thu': 4,
               'Fri': 5,
               'Sat': 6}

def init_sample_sent_events(apps, schema_editor):
    sample_sent_events = \
[
    { "title": "Up for brunch Sunday?",
        "venue": "Zazie",
        "address": "941 Cole St, San Francisco, CA 94117",
        "evt_date": "Sun 1PM",
        "city": "San Francisco"
    },
    { "title": "Drinks Friday Night, are you in?",
        "venue": "Press Club",
        "address": "25 Yerba Buena Lane, San Francisco, CA 94103",
        "evt_date": "Fri 8PM",
        "city": "San Francisco"
    },
    { "title": "Game of Thrones, let's watch at my place", 
        "venue": "my place", 
        "address": "insert address",
        "evt_date": "Sun 9PM",
        "city": "Anywhere"
    }
]
    for evt in sample_sent_events:
        evt_date_str = evt["evt_date"]
        _now = datetime.now(tz=pytz.timezone('US/Pacific'))
        _now = _now.replace(hour=datetime.strptime(evt_date_str[evt_date_str.index(' ') + 1:], '%I%p').hour, minute=0)
        if _now.weekday() < WEEKDAY_IDX[evt_date_str[:3]]:
            evt_date = _now + timedelta(days=WEEKDAY_IDX[evt_date_str[:3]] - _now.weekday())
        elif _now.weekday() == WEEKDAY_IDX[evt_date_str[:3]]:
            evt_date = _now + timedelta(days=7)
        else:
            evt_date = _now + timedelta(days=6 - (_now.weekday() - WEEKDAY_IDX[evt_date_str[:3]]))
        sample_evt = SampleEvent(type='sent',
                                 title=evt["title"],
                                 address=evt['address'],
                                 event_date=evt_date.astimezone(pytz.utc),
                                 venue_name=evt["venue"],
                                 city=evt['city'])
        sample_evt.save()

def init_sample_received_events(apps, schema_editor):
    sample_received_events = \
[
	{
		"title": "Want to join us for lunch?",
		"venue": "Amigo HQ",
		"address": "San Francisco, CA 94117",
		"other_invitees": "",
		"evt_date": "Fri 1PM",
        "city": "San Francisco"
	}
]
            
    for evt in sample_received_events:
        evt_date_str = evt["evt_date"]
        _now = datetime.now(tz=pytz.timezone('US/Pacific'))
        _now = _now.replace(hour=datetime.strptime(evt_date_str[evt_date_str.index(' ') + 1:], '%I%p').hour, minute=0)
        if _now.weekday() < WEEKDAY_IDX[evt_date_str[:3]]:
            evt_date = _now + timedelta(days=WEEKDAY_IDX[evt_date_str[:3]] - _now.weekday())
        elif _now.weekday() == WEEKDAY_IDX[evt_date_str[:3]]:
            evt_date = _now + timedelta(days=7)
        else:
            evt_date = _now + timedelta(days=6 - (_now.weekday() - WEEKDAY_IDX[evt_date_str[:3]]))
        sample_evt = SampleEvent(type='received',
                                 title=evt["title"],
                                 address=evt['address'],
                                 event_date=evt_date.astimezone(pytz.utc),
                                 venue_name=evt["venue"],
                                 city=evt['city'])
        sample_evt.save()


class Migration(migrations.Migration):

    dependencies = [
        # migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('events', '0018_auto_20160309_0114'),
    ]


    operations = [
        migrations.CreateModel(
            name='SampleEvent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='Created', editable=False, blank=True)),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='Modified', editable=False, blank=True)),
                ('title', models.CharField(max_length=250, verbose_name='Title')),
                ('event_date', models.DateTimeField(verbose_name='Created Date')),
                ('address', models.TextField(default=b'',verbose_name='Address')),
                ('location', django_extensions.db.fields.json.JSONField(blank=True, null=True)),
                ('venue_name', models.CharField(blank=True, verbose_name='Venue Name', max_length=100)),
                ('city', models.CharField(blank=True, null=True, verbose_name='City', max_length=200)),
                ('type', models.CharField(blank=False, verbose_name='Type', max_length=10))
            ],
            options={
                'ordering': ['-created'],
                'verbose_name': 'Sample sent/received event',
                'verbose_name_plural': 'Sample sent/received events',
            },
            bases=(models.Model,),
        ),
        migrations.RunPython(init_sample_sent_events),
        migrations.RunPython(init_sample_received_events)
    ]

