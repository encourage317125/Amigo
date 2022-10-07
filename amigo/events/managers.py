# Standard Library
from datetime import timedelta

# Third Party Stuff
from django.db import models
from django.db.models import Q
from django.utils.timezone import now


class InvitationQuerySet(models.QuerySet):
    def upcoming(self):
        return self.filter((Q(event__is_time_specified=True) & Q(event__event_date__gte=now() - timedelta(hours=2))) |
                           (Q(event__is_time_specified=False) & Q(event__event_date__gte=now() - timedelta(hours=12))))

    def expired(self):
        return self.filter((Q(event__is_time_specified=True) & Q(event__event_date__lt=now() - timedelta(hours=2))) |
                           (Q(event__is_time_specified=False) & Q(event__event_date__lt=now() - timedelta(hours=12))))


class EventQuerySet(models.QuerySet):
    def upcoming(self):
        return self.filter((Q(is_time_specified=True) & Q(event_date__gte=now() - timedelta(hours=2))) |
                           (Q(is_time_specified=False) & Q(event_date__gte=now() - timedelta(hours=12))))

    def expired(self):
        return self.filter((Q(is_time_specified=True) & Q(event_date__lt=now() - timedelta(hours=2))) |
                           (Q(is_time_specified=False) & Q(event_date__lt=now() - timedelta(hours=12))))
