# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

# Third Party Stuff
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible
from django.utils.functional import cached_property
from django.utils.translation import ugettext_lazy as _
from django_extensions.db.models import TimeStampedModel
from django_i18n_utils.models import UnicodeNormalizerMixin
from jsonfield import JSONField
from model_utils import Choices, FieldTracker

# Amigo Stuff
from amigo.base.fields import PhoneNumberField

from . import managers


# TO DO: RSVP Related?
@python_2_unicode_compatible
class Invitation(models.Model, UnicodeNormalizerMixin):
    APP_USER = 0
    PASSIVE_USER = 1
    NEW_USER = 2

    STATUSES = (
        (APP_USER, 'App User'),
        (PASSIVE_USER, 'Passive User'),
        (NEW_USER, 'New User'),
    )

    # This model stores all event invitations, with or without an assigned user.
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, default=None,
                             related_name="invitations")

    # This will log user status to see how conversions occur through time,
    # And the typical invitation status of invitees from a user
    invitee_current_status = models.IntegerField(default=APP_USER, choices=STATUSES,
                                                 help_text='This allows querying invitation \
                                                            status based on user action for analytics.')

    event = models.ForeignKey("Event", null=False, blank=False,
                              related_name="invitations")
    # necessary???
    is_owner = models.BooleanField(default=False, null=False, blank=False)

    # Invitation metadata
    phone_number = PhoneNumberField(default=None, null=True, blank=True,
                                    verbose_name=_("phone number"))
    created = models.DateTimeField(default=timezone.now,
                                   verbose_name=_("created at"))
    invited_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="ihaveinvited",
                                   null=True, blank=True)
    has_accepted_invite = models.NullBooleanField(default=None)
    has_seen = models.BooleanField(default=False, null=False, blank=False)
    rsvp_message = models.CharField(max_length=60, null=True, blank=True,
                                    help_text='message sent while reponding to this invitation.')
    rsvp_time = models.DateTimeField(null=True, blank=True)

    objects = managers.InvitationQuerySet.as_manager()

    def clean(self):
        if self.has_accepted_invite and not self.has_seen:
            self.has_seen = True

        if self.invited_by != self.event.owner:
            raise ValidationError(_('This user is not allowed to invite users to the event'))

        # TODO: Further Review
        if self.user:
            if self.phone_number is None:
                self.phone_number = self.user.phone_number
        else:
            invitations = Invitation.objects.filter(phone_number=self.phone_number, event=self.event)
            if invitations.count() > 0 and not self.id:
                raise ValidationError(_('The user is already invited in the event'))

    def save(self, *args, **kwargs):
        self.clean()
        return super(Invitation, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "invitation"
        verbose_name_plural = "invitations"
        app_label = "events"
        unique_together = (("user", "event"),)
        ordering = ["event", "user__full_name", "user__phone_number"]
        permissions = (
            ("view_invitation", "Can view invitation"),
        )

    def __str__(self):
        return '{} by {} to {}'.format(self.event.title, self.invited_by, self.user)


@python_2_unicode_compatible
class SampleRSVPReply(TimeStampedModel, UnicodeNormalizerMixin):

    '''
    To store random list of possible positvie and negative responses that a user
    can use while replying to a invitation.
    '''
    RSVP_TYPE = Choices('accept', 'reject')
    text = models.CharField(blank=False, null=False, max_length=60, unique=True)
    type = models.CharField(blank=False, null=False, choices=RSVP_TYPE, max_length=10)

    def clean(self):
        self.text = self.text.strip()

    def __str__(self):
        return '{} ({})'.format(self.text, self.type)

    class Meta:
        verbose_name = "sample RSVP message"
        app_label = "events"
        verbose_name_plural = "sample RSVP messages"
        ordering = ['type', 'text']


@python_2_unicode_compatible
class Event(TimeStampedModel, UnicodeNormalizerMixin):
    title = models.CharField(max_length=250, null=False, blank=False,
                             verbose_name=_("title"))
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, null=False, blank=False,
                              related_name="owned_events", verbose_name=_("owner"))
    event_date = models.DateTimeField(null=False, blank=False,
                                      verbose_name=_("event date"))
    is_time_specified = models.BooleanField(null=False, blank=True, default=True,
                                            help_text='whether "event_date" contains a specific time of day.')
    invitees = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="events",
                                      through="Invitation", verbose_name=_("invitees"),
                                      through_fields=("event", "user"))
    location = JSONField(default={}, blank=True)
    address = models.TextField(null=False, blank=True, default='')
    venue_name = models.CharField(max_length=100, null=False, blank=True,
                                  verbose_name=_("venue name"))
    reminder_sent = models.BooleanField(default=False, blank=True, null=False,
                                        help_text=_('whether upcoming event reminder sent or not.'))
    is_canceled = models.BooleanField(null=False, blank=False, default=False,
                                      help_text='whether or not this event was canceled')
    tracker = FieldTracker()

    objects = managers.EventQuerySet.as_manager()

    class Meta:
        verbose_name = _(u'event')
        verbose_name_plural = _(u'events')
        app_label = "events"
        ordering = ['-event_date', 'title']
        permissions = (
            ("view_event", "Can view event"),
        )

    def __str__(self):
        return self.title

    @cached_property
    def invitations_count(self):
        return Invitation.objects.filter(event=self).count()

    @cached_property
    def invitees_list(self):
        return ",".join([str(p) for p in self.invitees.all()])

    @property
    def attendees_count(self):
        return Invitation.objects.filter(event=self, has_accepted_invite=True).count()

    def clean(self):
        pass

    def save(self, *args, **kwargs):
        self.clean()
        return super(Event, self).save(*args, **kwargs)

    def cancel(self):
        self.is_canceled = True
        self.save()


@python_2_unicode_compatible
class SampleEvent(TimeStampedModel, UnicodeNormalizerMixin):
    title = models.CharField(max_length=250, null=False, blank=False,
                             verbose_name=_("Title"))
    event_date = models.DateTimeField(null=False, blank=False,
                                      verbose_name=_("Event Date"))
    location = JSONField(default={}, blank=True)
    address = models.TextField(null=False, blank=True, default='')
    venue_name = models.CharField(max_length=200, null=False, blank=True,
                                  verbose_name=_("Venue Name"))
    city = models.CharField(max_length=200, null=True, blank=True,
                            verbose_name=_("City"))
    type = models.CharField(blank=False,
                            verbose_name='Type',
                            max_length=10)

    class Meta:
        verbose_name = _(u'Sample Event')
        verbose_name_plural = _(u'Sample Events')
        app_label = "events"
        permissions = (("view_event", "Can view event"),)

    def __str__(self):
        return self.title


@python_2_unicode_compatible
class InviteText(models.Model, UnicodeNormalizerMixin):
    invite_text = models.CharField(max_length=800, null=False, blank=False,
                                   verbose_name=_("Invite Text"))

    class Meta:
        verbose_name = _(u'Invite Text')
        verbose_name_plural = _(u'Invite Texts')
        app_label = "events"
        # permissions = (("view_event", "Can view event"),)

    def __str__(self):
        return self.linkify(self.invite_text)
