# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

# Third Party Stuff
from amigo.users.models import User
from django.core.management.base import BaseCommand
from optparse import make_option


class Command(BaseCommand):
    args = '<phone_number phone_number ...>'
    help = 'Delete users with phone numbers'

    def add_arguments(self, parser):
        parser.add_argument('phone', nargs='+', type=str)

    option_list = BaseCommand.option_list + (
        make_option('--all',
                    action='store_true',
                    dest='all',
                    default=False,
                    help='Delete all regular, non-admin users'),
                   )

    def handle(self, *args, **options):
        if options['all']:
            self.stdout.write('  Deleting all regular users, not superusers')
            User.objects.filter(is_superuser=False).delete()
        else:
            self.stdout.write('  Deleting users with phone numbers: {0}.'.format(args))
            for phone in args:
                try:
                    user = User.objects.get(phone_number=phone)
                    self.stdout.write('  Deleting user with phone number: {0}.'.format(phone))
                    user.delete()
                except User.DoesNotExist:
                    pass
