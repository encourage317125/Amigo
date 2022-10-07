# -*- coding: utf-8 -*-
# Standard Library
import os

# Third Party Stuff
import django
import pytest

from .fixtures import *  # noqa

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
os.environ.setdefault("DEBUG", "True")
os.environ.setdefault("DJANGO_SITE_DOMAIN", "Testing")


def pytest_addoption(parser):
    parser.addoption("--runslow", action="store_true", help="run slow tests")


def pytest_runtest_setup(item):
    if "slow" in item.keywords and not item.config.getoption("--runslow"):
        pytest.skip("need --runslow option to run")


def pytest_configure(config):
    # make sure encoding is set to utf-8
    # http://stackoverflow.com/a/21190382/782901
    import sys
    reload(sys)
    sys.setdefaultencoding('utf8')
    django.setup()
