# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import random

# Third Party Stuff
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser
from django.db import models
from django.dispatch import receiver
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from django_i18n_utils.models import UnicodeNormalizerMixin
from django_i18n_utils.utils import clean_unicode
from jsonfield import JSONField

# Amigo Stuff
from amigo.base.fields import PhoneNumberField
from amigo.base.models import PhotoMixin

from . import managers


class PermissionsMixin(models.Model):
    """
    A mixin class that adds the fields and methods necessary to support
    Django's Permission model using the ModelBackend.
    """
    is_superuser = models.BooleanField(_('superuser status'), default=False,
                                       help_text=_('Designates that this user has all permissions without '
                                                   'explicitly assigning them.'))

    class Meta:
        abstract = True

    def has_perm(self, perm, obj=None):
        """Returns True if the user is superadmin and is active
        """
        return self.is_active and self.is_superuser

    def has_perms(self, perm_list, obj=None):
        """Returns True if the user is superadmin and is active
        """
        return self.is_active and self.is_superuser

    def has_module_perms(self, app_label):
        """Returns True if the user is superadmin and is active
        """
        return self.is_active and self.is_superuser

    @property
    def is_staff(self):
        return self.is_superuser


class UserDefaults(models.Model):
    notify_new_invite = models.BooleanField(default=True, null=False)
    notify_invite_rsvp = models.BooleanField(default=True, null=False)
    notify_contact_joined = models.BooleanField(default=True, null=False)
    notify_event_full = models.BooleanField(default=True, null=False)
    notify_upcoming_event = models.BooleanField(default=True, null=False)

    class Meta:
        abstract = True


@python_2_unicode_compatible
class User(UserDefaults, PhotoMixin, AbstractBaseUser, PermissionsMixin, UnicodeNormalizerMixin):
    phone_number = PhoneNumberField(unique=True, db_index=True)
    full_name = models.CharField(_('full name'), max_length=256, blank=True)
    email = models.EmailField(_('email address'), max_length=255, blank=True)
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    is_active = models.BooleanField(_('active'), default=True,
        help_text=_('Designates whether this user should be treated as active. '  # noqa
                    'Unselect this instead of deleting accounts.'))
    phonebook_phone_numbers = JSONField(default=[])
    objects = managers.UserManager()
    is_app_user = models.BooleanField(_('app_user'), default=False)
    first_interaction = models.DateTimeField(_('first_interaction'), default=None, null=True)
    fb_token = models.CharField(_('facebook access token'), max_length=512, blank=True, null=True)

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = "user"
        verbose_name_plural = "users"
        ordering = ["full_name"]
        permissions = (
            ("view_user", "Can view user"),
        )

    def __str__(self):
        return clean_unicode(self.get_full_name())

    def get_short_name(self):
        '''Returns the short name for the user.

        Format: {first_name} {first_letter_of_last_name}
        '''
        words = self.full_name.strip().split(' ')
        if len(words) == 1:
            # user only has first name, return it.
            return self.full_name
        last_name = words.pop()
        short_name = '{} {}'.format(words[0], last_name[0])
        return clean_unicode(short_name)

    def get_full_name(self):
        name = self.full_name or self.phone_number or self.email
        return clean_unicode(name)

    # If user doesn't have a profile image, randomly choose a smiley
    # from the smiley folder
    @property
    def photo_url(self):
        if self.photo and hasattr(self.photo, 'url'):
            return self.photo.url
        elif self.photo_uri:
            return self.photo_uri
        else:
            lst = ['default-face@3x.png',
                   'glasses-face@3x.png',
                   'megasmile-face@3x.png',
                   'pirate-face@3x.png',
                   'tongue-face@3x.png']
            smiley = random.choice(lst)
            # smiley = random.choice(os.listdir(os.path.join(settings.STATIC_ROOT, 'smileys'))).strip()
            return settings.STATIC_URL+'smileys/{}'.format(smiley)

    def delete(self):
        if self.pk:
            events = self.events.all()
            if events:
                for event in events:
                    if len(event.invitees.all()) == 1 and event.invitees.first().pk == self.pk:
                        event.delete()
        super(User, self).delete()


# http://stackoverflow.com/questions/6377631/how-to-override-the-default-value-of-a-model-field-from-an-abstract-base-class
# Django doesn't seem to support overwriting inherited classes
User._meta.get_field('last_login').default = None
User._meta.get_field('last_login').null = True


@python_2_unicode_compatible
class FavoriteContact(models.Model):
    phone_number = PhoneNumberField(db_index=True)
    owner = models.ForeignKey(User, null=False, blank=False,
                              related_name="contacts", verbose_name=_("owner"),
                              help_text="This contact belongs to this user's phonebook")
    created = models.DateTimeField(_('created'), default=timezone.now)

    def __str__(self):
        return '{}'.format(self.phone_number)

    class Meta:
        verbose_name = "favorite contact"
        verbose_name_plural = "favorite contacts"
        ordering = ['owner', '-created']
        unique_together = ['phone_number', 'owner']


# A new user is created, update any invitations that he might be
# part of before he joined.
@receiver(models.signals.post_save, sender=User, dispatch_uid="role_post_save")
def user_post_save(sender, instance, created, **kwargs):
    user = instance

    # ignore if object is just created
    if created:
        from amigo.events.services import associate_user_to_invites
        associate_user_to_invites(user)
