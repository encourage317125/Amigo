# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

# Third Party Stuff
from django import forms
from django.contrib.auth.forms import UserCreationForm as DjangoUserCreationForm

from .models import User


class UserCreationForm(DjangoUserCreationForm):
    def clean_phone_number(self):
        # Since User.phone_number is unique, this check is redundant,
        # but it sets a nicer error message than the ORM. See #13147.
        phone_number = self.cleaned_data["phone_number"]
        try:
            User._default_manager.get(phone_number=phone_number)
        except User.DoesNotExist:
            return phone_number
        raise forms.ValidationError(self.error_messages['duplicate_phone_number'])

    class Meta:
        model = User
        fields = ('phone_number',)
