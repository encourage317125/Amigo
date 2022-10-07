# -*- coding: utf-8 -*-

# Third Party Stuff
from django.contrib.auth.models import BaseUserManager
from django.utils.timezone import now


class UserManager(BaseUserManager):

    def create_user(self, phone_number, password=None, **extra_fields):
        '''Creates and saves a User with the given phone_number and password.
        '''
        if not phone_number:
            raise ValueError('Phone number must be set')

        if 'email' in extra_fields:
            extra_fields['email'] = UserManager.normalize_email(
                extra_fields['email'])

        if 'is_active' not in extra_fields:
            extra_fields['is_active'] = True

        user = self.model(phone_number=phone_number, is_staff=False, is_superuser=False,
                          **extra_fields)
        user.last_login = now()
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, password, **extra_fields):
        '''Creates and saves a User with the given email and password and set it
        as a superuser.
        '''
        user = self.create_user(phone_number, password, **extra_fields)
        user.is_active = True
        user.is_superuser = True
        user.save(using=self._db)
        return user
