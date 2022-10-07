# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

# Standard Library
import random
from datetime import datetime, timedelta

# Third Party Stuff
import factory
from django.conf import settings


class Factory(factory.DjangoModelFactory):
    class Meta:
        strategy = factory.CREATE_STRATEGY
        model = None
        abstract = True


class UserFactory(Factory):
    class Meta:
        model = settings.AUTH_USER_MODEL
        strategy = factory.CREATE_STRATEGY

    full_name = factory.Sequence(lambda n: "User😈 {}".format(n))
    phone_number = factory.Sequence(lambda n: '+91837708%04d' % n)
    email = factory.Sequence(lambda n: 'user%04d@email.com' % n)
    password = factory.PostGeneration(lambda obj, *args, **kwargs: obj.set_password(obj.phone_number))
    photo = factory.django.ImageField(color='blue')
    last_login = factory.LazyAttribute(lambda o: datetime.today() - timedelta(days=random.randrange(1, 20)))


class AttendeeFactory(Factory):
    class Meta:
        model = "events.Invitation"
        strategy = factory.CREATE_STRATEGY

    event = factory.SubFactory("tests.factories.EventFactory")
    user = factory.SubFactory("tests.factories.UserFactory")
    invited_by = factory.SubFactory("tests.factories.UserFactory")


class FavoriteContactFactory(Factory):
    class Meta:
        model = "users.FavoriteContact"
        strategy = factory.CREATE_STRATEGY
    owner = factory.SubFactory("tests.factories.UserFactory")
    phone_number = factory.Sequence(lambda n: '+91837708%04d' % n)


class EventFactory(Factory):
    class Meta:
        model = "events.Event"
        strategy = factory.CREATE_STRATEGY

    title = factory.Sequence(lambda n: "Event☔️ {}".format(n))
    event_date = factory.LazyAttribute(lambda o: datetime.today() + timedelta(days=random.randrange(1, 20)))
    owner = factory.SubFactory("tests.factories.UserFactory")


class EventInviteTextFactory(Factory):
    class Meta:
        model = "events.InviteText"
        strategy = factory.CREATE_STRATEGY

    invite_text = factory.Sequence(lambda n: "Invite Text {}".format(n))


class SampleRSVPReplyFactory(Factory):
    class Meta:
        model = "events.SampleRSVPReply"
        strategy = factory.CREATE_STRATEGY

    text = factory.Sequence(lambda n: "Reply Message🐙 {}".format(n))


class InvitationFactory(Factory):
    class Meta:
        model = "events.Invitation"
        strategy = factory.CREATE_STRATEGY

    user = factory.SubFactory("tests.factories.UserFactory")
    event = factory.SubFactory("tests.factories.EventFactory")
    phone_number = factory.Sequence(lambda n: '+91987700%04d' % n)
    invited_by = factory.SubFactory("tests.factories.UserFactory")


def create_event(**kwargs):
    "Create a event along with its dependencies"
    defaults = {}
    defaults.update(kwargs)

    event = EventFactory.create(**defaults)

    return event


def create_user(**kwargs):
    "Create an user along with her dependencies"
    return UserFactory.create(**kwargs)
