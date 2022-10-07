# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# Third Party Stuff
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models

# Amigo Stuff
import amigo.base.fields


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_user_phonebook_phone_numbers'),
    ]

    operations = [
        migrations.CreateModel(
            name='FavoriteContact',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_number', amigo.base.fields.PhoneNumberField(max_length=128, db_index=True)),
                ('created', models.DateTimeField(default=django.utils.timezone.now, verbose_name='created')),
                ('owner', models.ForeignKey(related_name='contacts', to=settings.AUTH_USER_MODEL, verbose_name='owner', help_text="This contact belongs to this user's phonebook")),
            ],
            options={
                'ordering': ['owner', '-created'],
                'verbose_name_plural': 'favorite contacts',
                'verbose_name': 'favorite contact',
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='favoritecontact',
            unique_together=set([('phone_number', 'owner')]),
        ),
    ]
