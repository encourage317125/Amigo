# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

# Third Party Stuff
from phonenumber_field.modelfields import PhoneNumberDescriptor as _PhoneNumberDescriptor
from phonenumber_field.modelfields import PhoneNumberField as _PhoneNumberField


class PhoneNumberDescriptor(_PhoneNumberDescriptor):

    def __get__(self, instance=None, owner=None):
        '''This is here to de-serialize the phone number as string instead
        of `PhoneNumber` object.
        '''
        value = super(self.__class__, self).__get__(instance, owner)
        return str(value) if value else value


class PhoneNumberField(_PhoneNumberField):
    descriptor_class = PhoneNumberDescriptor
