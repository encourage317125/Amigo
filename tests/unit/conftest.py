# Third Party Stuff
from django.conf import settings

from ..utils import disconnect_signals


def pytest_runtest_setup(item):
    settings.DISABLE_PUSH_NOTIFICATION = True
    settings.TWILIO_DRY_MODE = True
    settings.TWILIO_CALLBACK_DOMAIN = "testserver"
    settings.TWILIO_ACCOUNT_SID = "AC4ea708fa669d186b4f1c422ba4d27740"
    settings.TWILIO_AUTH_TOKEN = "6b8f162a89363e3fbb4b779a21b952a4"
    settings.TWILIO_PHONE_NUMBER = "+14755292729"
    disconnect_signals()
