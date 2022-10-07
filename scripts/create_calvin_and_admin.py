# -*- coding: utf-8 -*-

from django.core.files import File
from tests.factories import UserFactory


def run(*args):
    image = open('./static/calvin.jpg')
    UserFactory(phone_number='+15627408020',
                full_name='Calvin Broadus',
                email='paul+calvin@amigo.io',
                photo=File(image, 'r'))
    image = open('./static/alan_smithee.jpg')
    UserFactory(phone_number='+14157988586',
                full_name='Alan Smithee',
                email='alansmithee@email.com',
                photo=File(image, 'r'))

    u = UserFactory(full_name='Amigo Administrator',
                    email='alldev@amigo.io',
                    phone_number='+14155551111')
    u.set_password('amigo')
    u.is_superuser = True
    u.save()
