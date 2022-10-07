# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

# Third Party Stuff
from optparse import make_option
from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.core.files import File
from django.utils import timezone
from django.utils.timezone import now

from amigo.users.models import User, FavoriteContact
from amigo.events.models import Event, Invitation
from amigo.events.services import add_bulk_invitation_by_phone
from amigo.notifications.models import EventToken


class Command(BaseCommand):
    help = 'Create sample data'

    option_list = BaseCommand.option_list + (
        make_option('--clean',
                    action='store_true',
                    dest='clean',
                    default=False,
                    help='Clean all test users, including created by tests'),
                   )

    def handle(self, *args, **options):
        joniMitchelPhone = '+12019485595'
        acidPauliPhone = '+14155551970'
        alanSmitheePhone = '+15627408020'
        johnAppleseedPhone = '+18885555512'
        danielHigginsPhone = '+14085555270'
        kateBellPhone = '+14155553695'

        if options['clean']:
            phones = [alanSmitheePhone, johnAppleseedPhone, joniMitchelPhone, danielHigginsPhone, acidPauliPhone]
            call_command('delete_user', *phones)
        self.stdout.write('  Creating sample data')
        calvin = User(phone_number=johnAppleseedPhone,
                      first_interaction=now(),
                      full_name='Calvin Broadus',
                      email='paul+calvin@amigo.io',
                      photo=File(open('./static/calvin.jpg'), 'r'),
                      last_login=now())
        calvin.save()
        alan = User(phone_number=alanSmitheePhone,
                    first_interaction=now(),
                    full_name='Alan Smithee',
                    email='alansmithee@email.com',
                    photo=File(open('./static/alan_smithee.jpg'), 'r'),
                    last_login=now())
        alan.save()
        get_together = Event(id=8888881,
                             title='Get together',
                             owner=calvin,
                             event_date=timezone.datetime(2017, 1, 19, tzinfo=timezone.utc))
        get_together.save()
        picnic = Event(title='Picnic',
                       owner=alan,
                       venue_name='Dolores Park',
                       event_date=timezone.datetime(2017, 2, 28, hour=20, tzinfo=timezone.utc))
        picnic.save()
        Invitation(user=calvin, event=picnic, has_accepted_invite=None, invited_by=picnic.owner).save()
        movies = Event(title='Movies and Popcorn',
                       owner=alan,
                       venue_name='AMC',
                       address='1000 Van Ness Ave, San Francisco, CA  94109, United States',
                       event_date=timezone.datetime(2017, 3, 8, hour=4, tzinfo=timezone.utc))
        movies.save()
        Invitation(user=calvin, event=movies, has_accepted_invite=True, invited_by=movies.owner).save()
        daniel = User(phone_number=danielHigginsPhone,
                      first_interaction=now(),
                      photo=File(open('./static/daniel_higgins.jpg'), 'r'),
                      last_login=now())
        daniel.save()
        Invitation(user=daniel, event=movies, has_accepted_invite=None, invited_by=movies.owner).save()
        acidPauli = User(phone_number=acidPauliPhone,
                         first_interaction=now(),
                         last_login=now())
        acidPauli.save()
        Invitation(user=acidPauli,
                   event=movies,
                   has_accepted_invite=False,
                   invited_by=movies.owner,
                   rsvp_message="Sorry, already have other plans").save()

        evt_token = EventToken(user=calvin, event=get_together, token='fdsa')
        evt_token.save()

        add_bulk_invitation_by_phone(event=get_together,
                                     phone_numbers=[alanSmitheePhone,
                                                    joniMitchelPhone,
                                                    danielHigginsPhone,
                                                    acidPauliPhone],
                                     invited_by=calvin)
        pauliInvite = Invitation.objects.get(user_id=acidPauli.id, event_id=get_together.id)
        pauliInvite.has_accepted_invite = True
        pauliInvite.rsvp_message = "Let's party, it's Acid Sunday!"
        pauliInvite.save()

        FavoriteContact(phone_number=danielHigginsPhone, owner=alan).save()
        FavoriteContact(phone_number=kateBellPhone, owner=alan).save()
