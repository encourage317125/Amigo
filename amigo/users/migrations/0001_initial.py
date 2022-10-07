# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# Third Party Stuff
import django.utils.timezone
from django.db import migrations, models

# Amigo Stuff
import amigo.base.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('password', models.CharField(verbose_name='password', max_length=128)),
                ('last_login', models.DateTimeField(verbose_name='last login', default=django.utils.timezone.now)),
                ('is_superuser', models.BooleanField(verbose_name='superuser status', help_text='Designates that this user has all permissions without explicitly assigning them.', default=False)),
                ('phone_number', amigo.base.fields.PhoneNumberField(unique=True, db_index=True, max_length=128)),
                ('full_name', models.CharField(blank=True, verbose_name='full name', max_length=256)),
                ('email', models.EmailField(blank=True, verbose_name='email address', max_length=255, unique=True)),
                ('date_joined', models.DateTimeField(verbose_name='date joined', default=django.utils.timezone.now)),
                ('is_active', models.BooleanField(verbose_name='active', help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', default=True)),
            ],
            options={
                'permissions': (('view_user', 'Can view user'),),
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'ordering': ['full_name'],
            },
            bases=(models.Model,),
        ),
    ]
