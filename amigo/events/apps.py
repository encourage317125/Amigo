# -*- coding: utf-8 -*-

# Third Party Stuff
from django.apps import AppConfig, apps
from django.db.models import signals

from . import signals as handlers


class EventsAppConfig(AppConfig):
    name = "amigo.events"
    verbose_name = "Events"

    def ready(self):
        # New Event
        # uncomment the line below to add event owner to list of attendee
        # signals.post_save.connect(handlers.add_event_owner_in_attendee_list,
        #                           sender=apps.get_model("events", "Event"))
        signals.post_save.connect(handlers.notify_event_detail_change,
                                  sender=apps.get_model("events", "Event"))
        signals.post_save.connect(handlers.clear_event_invitation_caches,
                                  sender=apps.get_model("events", "Invitation"))
        signals.post_save.connect(handlers.track_new_event_created,
                                  sender=apps.get_model("events", "Event"))
        signals.post_save.connect(handlers.track_new_invitation_created,
                                  sender=apps.get_model("events", "Invitation"))
