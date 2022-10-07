from datetime import datetime, timedelta
from amigo.pages.templatetags.app_filters import friendly_timestamp
from mock import MagicMock, patch


def test_friendly_timestamp_this_week():
    ut_timestamp = datetime.strptime('Fri Mar 11 08:05:43 2016', '%c')
    evt_timestamp = ut_timestamp + timedelta(days=1)

    with patch('amigo.pages.templatetags.app_filters.datetime', return_value=MagicMock()) as mock_dt:
        mock_dt.utcnow.return_value = ut_timestamp
        assert friendly_timestamp(evt_timestamp) == 'This Sat 08:05AM'


def test_friendly_timestamp_next_week():
    ut_timestamp = datetime.strptime('Sat Mar 12 08:05:43 2016', '%c')
    evt_timestamp = ut_timestamp + timedelta(days=7)

    with patch('amigo.pages.templatetags.app_filters.datetime', return_value=MagicMock()) as mock_dt:
        mock_dt.utcnow.return_value = ut_timestamp
        assert friendly_timestamp(evt_timestamp) == 'Next Sat Mar 19 08:05AM'
