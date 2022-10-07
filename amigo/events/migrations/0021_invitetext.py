# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django_i18n_utils.models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0020_auto_20160609_0121'),
    ]

    operations = [
        migrations.CreateModel(
            name='InviteText',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('invite_text', models.CharField(max_length=800, verbose_name='Invite Text')),
            ],
            options={
                'verbose_name': 'Invite Text',
                'verbose_name_plural': 'Invite Texts',
            },
            bases=(models.Model, django_i18n_utils.models.UnicodeNormalizerMixin),
        ),
        migrations.RunSQL("INSERT INTO events_invitetext (invite_text) VALUES ('{organizer} wants to know if you''re up for {event_title}. They are using Amigo, the easiest way to rally friends out. Details here: {event_link}');"),
        migrations.RunSQL("INSERT INTO events_invitetext (invite_text) VALUES ('{organizer} invited you to {event_title} via Amigo, it''s the easiest way to rally friends out. Deets here: {event_link}');"),
        migrations.RunSQL("INSERT INTO events_invitetext (invite_text) VALUES ('{organizer} wants to know if you''re up for {event_title}. They are using Amigo, the easiest way to get friends together. Here are the details: {event_link}');"),
        migrations.RunSQL("INSERT INTO events_invitetext (invite_text) VALUES ('{organizer} invited you to {event_title} via Amigo, it''s the fastest way to get friends together. Details here {event_link}');"),
        migrations.RunSQL("INSERT INTO events_invitetext (invite_text) VALUES ('{organizer} wants to know if you''re up for {event_title}. Get the details: {event_link}. Sent via Amigo, the fastest way to get friends together.');"),
        migrations.RunSQL("INSERT INTO events_invitetext (invite_text) VALUES ('{organizer} invited you to {event_title}, get the details {event_link}. Sent via Amigo, the easiest way to get friends together');"),
        migrations.RunSQL("INSERT INTO events_invitetext (invite_text) VALUES ('{organizer} wants to know if you''re up for {event_title}.  They are using Amigo because group texts suck. Details here: {event_link}');"),
        migrations.RunSQL("INSERT INTO events_invitetext (invite_text) VALUES ('{organizer} invited you to {event_title}. Deets here: {event_link}. Sent via Amigo because group texts suck.');"),
    ]
