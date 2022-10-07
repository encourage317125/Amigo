# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals
import random
import os
import csv
import urllib

# Third Party Stuff
# from optparse import make_option
# from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.core.files import File
from django.conf import settings

# Amigo Stuff
from amigo.users.models import User
# from amigo.events.models import Event


class Command(BaseCommand):
    help = 'Create/update sample user data from sample_users.csv'

    def __random_phone_num(self):
        n = '0000000000'
        while '9' in n[3:6] or n[3:6] == '000' or n[6] == n[7] == n[8] == n[9]:
            n = str(random.randint(10**9, 10**10-1))
        return '+1' + n[:3] + n[3:6] + n[6:]

    def handle(self, *args, **options):
        with open(os.path.join(settings.APP_DIR, 'sample_users.csv'), 'r') as csv_file:
            csv_data = csv.reader(csv_file)
            for user_data in csv_data:
                if csv_data.line_num == 1:
                    continue  # Ignore the CSV header

                if len(user_data) != 2:
                    print("WARNING: incorrect line in sample_users.csv, will ignore...")
                    print(','.join(user_data))
                    continue
                name = user_data[0]
                photo_url = user_data[1]
                result = urllib.urlretrieve(photo_url)
                if len(User.objects.filter(full_name=name)):
                    print("Found existing user: {}, updating its photo URL".format(name.decode('ascii', 'ignore')))
                    exist_user = User.objects.filter(full_name=name).first()
                    # exist_user.photo_url = photo_url
                    exist_user.photo.save(
                            os.path.basename(photo_url),
                            File(open(result[0])))
                    exist_user.save()
                else:
                    print("Creating new user: {}".format(name.decode('ascii', 'ignore')))
                    phone_num = self.__random_phone_num()
                    new_user = User(phone_number=phone_num,
                                    full_name=name,
                                    password=phone_num,
                                    photo_url=photo_url,
                                    email='')
                    new_user.save()
