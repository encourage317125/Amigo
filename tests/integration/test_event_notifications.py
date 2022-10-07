# -*- coding: utf-8 -*-
# Standard Library
from datetime import timedelta

# Third Party Stuff
import pytest
from django.utils.timezone import now
from mock import patch

# Amigo Stuff
from amigo.events.services import sent_event_reminders
from amigo.events.notification_services import send_invitation_sms
# from amigo.notifications.models import EventToken

from .. import factories as f

pytestmark = pytest.mark.django_db


def test_event_reminder_time_to_send():
    event = f.EventFactory.create(event_date=now() + timedelta(hours=25))
    with patch('amigo.events.notification_services.send_event_reminder_for_tomorrow') as sender:
        sent_event_reminders()
        sender.assert_called_once_with(event, [])
        sender.reset_mock()

        # should not reminder if run again
        sent_event_reminders()
        assert not sender.called

        # should not send any reminder if the event is less 24hr from now
        event.reminder_sent = False
        event.event_date = now() + timedelta(hours=23)
        event.save()
        sender.reset_mock()
        sent_event_reminders()
        assert not sender.called

        # should not send any reminder if the event is greater than 26hr from now
        event.reminder_sent = False
        event.event_date = now() + timedelta(hours=27)
        event.save()
        sender.reset_mock()
        sent_event_reminders()
        assert not sender.called


def test_event_reminder_who_to_send():
    owner = f.UserFactory()
    event = f.EventFactory.create(event_date=now() + timedelta(hours=25), owner=owner)
    invitation = f.InvitationFactory.create(event=event, has_accepted_invite=True, invited_by=owner)
    with patch('amigo.events.notification_services.send_event_reminder_for_tomorrow') as sender:
        sent_event_reminders()
        sender.assert_called_once_with(event, [invitation.user])

        invitation.has_accepted_invite = False
        event.reminder_sent = False
        event.save()
        invitation.save()
        sender.reset_mock()
        sent_event_reminders()
        sender.assert_called_once_with(event, [])


def test_sms_link():
    owner = f.UserFactory()
    event = f.EventFactory.create(owner=owner)
    f.EventInviteTextFactory.create(invite_text='sample invite text')
    phone_number = '+1 222 222-2222'

    with patch('amigo.events.notification_services.send_sms') as sender:
        send_invitation_sms(event, phone_number, owner)
        assert sender.called
        # _, kwargs = sender.call_args
        # print kwargs['body']
        # token = kwargs['body'].split('token=')[1]
        # eventToken = EventToken.objects.get(token=token)
        # assert eventToken.event == event
        # assert eventToken.user.phone_number == phone_number
