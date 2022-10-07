# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

# Third Party Stuff
from django.core.management.base import BaseCommand

# Amigo Stuff
from amigo.events.services import sent_event_reminders


class Command(BaseCommand):

    def handle(self, *args, **options):

        print('  Sending event reminders...')
        sent_event_reminders()
