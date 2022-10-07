# Third Party Stuff
from django.utils import six


def to_boolean(value):
    '''
    Tries to convert given 'value' to python boolean.
    '''
    if value is None:
        return None

    if isinstance(value, bool):
        return value

    if isinstance(value, six.string_types):
        value = value.lower()
        if value in ['true', 'y', 'yes', '1', 'ok']:
            return True
        elif value in ['false', 'n', 'no', '0']:
            return False

    # all attempt failed, shout-out loud!
    raise TypeError('Can not covert "%s" to boolean' % value)
