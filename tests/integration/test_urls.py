# from django.core.urlresolvers import reverse

# Third Party Stuff
import pytest

from .. import factories as f

pytestmark = pytest.mark.django_db


def test_api_root_is_protected(client):
    response = client.get('/api/')
    assert response.status_code == 401

    user = f.create_user(is_superuser=True, is_staff=True)
    client.login(user)
    response = client.get('/api/')
    assert response.status_code == 200


def test_admin_is_available(client):
    user = f.create_user(is_superuser=True, is_staff=True)
    client.login(user)
    response = client.get('/admin/')
    assert response.status_code == 200
