# Standard Library
import unittest
import urllib
from datetime import timedelta

# Third Party Stuff
import pytest
from django.core.urlresolvers import reverse
from django.utils.timezone import now

from .. import factories as f

pytestmark = pytest.mark.django_db


@unittest.skipIf(True, "Skip for now, will fix soon")
def test_api_events_feeedall(client):
    event = f.EventFactory.create(event_date=now() + timedelta(hours=1))

    params = {}

    url = reverse('events-feedall')
    client.login(event.owner)

    response = client.json.get(url + '?%s' % urllib.urlencode(params))
    assert response.status_code == 200

    # Check that the list is not paginated
    assert isinstance(response.data, list)
    assert len(response.data) == 1

    # Should respect time parameter
    params['cursor'] = response.data[-1]['event_date']
    resp = client.json.get(url + '?%s' % urllib.urlencode(params))
    assert len(resp.data) == 0

    # should work for recieved events
    params['type'] = 'received'
    response = client.json.get(url + '?%s' % urllib.urlencode(params))
    assert response.status_code == 200
