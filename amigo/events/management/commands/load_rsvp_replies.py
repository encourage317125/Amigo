# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

# Third Party Stuff
from django.core.management.base import BaseCommand
from django.db import transaction as tx

# Amigo Stuff
from amigo.events.models import SampleRSVPReply


class Command(BaseCommand):

    @tx.atomic
    def handle(self, *args, **options):

        print('  Adding default sample rsvp messages...')
        sample_rsvp_replies_for_accept = [
            "Count me in!",
            "I'll be there :)",
            "Let's go!",
            "RSVP",
            "Sounds lovely",
            "Sounds lovely",
            "Sure",
            "Without a doubt!",
            "Yesss!",
        ]
        sample_rsvp_replies_for_reject = [
            "I'll pass.",
            "Maybe next time!",
            "Nah, I'm good",
            "Nope",
            "Not for me :)",
            "Sorry, I can't",
            "Wish I could!",
            'No, thanks!',
        ]
        self.create_sample_rsvp_replies(positives=sample_rsvp_replies_for_accept,
                                        negatives=sample_rsvp_replies_for_reject)

    def create_sample_rsvp_replies(self, positives=[], negatives=[]):
        for text in positives:
            SampleRSVPReply.objects.get_or_create(text=text, type=SampleRSVPReply.RSVP_TYPE.accept)
        for text in negatives:
            SampleRSVPReply.objects.get_or_create(text=text, type=SampleRSVPReply.RSVP_TYPE.reject)
