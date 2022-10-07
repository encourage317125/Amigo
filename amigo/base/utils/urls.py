# -*- coding: utf-8 -*-

# Third Party Stuff
import arrow
import django_sites as sites
from django.core.urlresolvers import reverse as django_reverse

URL_TEMPLATE = "{scheme}://{domain}/{path}"


def build_url(path, scheme="http", domain="localhost"):
    return URL_TEMPLATE.format(scheme=scheme, domain=domain, path=path.lstrip("/"))


def is_absolute_url(path):
    """Test wether or not `path` is absolute url."""
    return path.startswith("http")


def get_absolute_url(path):
    """Return a path as an absolute url."""
    if is_absolute_url(path):
        return path
    site = sites.get_current()
    return build_url(path, scheme=site.scheme, domain=site.domain)


def reverse(viewname, *args, **kwargs):
    """Same behavior as django's reverse but uses django_sites to compute absolute url."""
    return get_absolute_url(django_reverse(viewname, *args, **kwargs))


def get_datetime_from_query_params(request, param):
    '''return datetime object from a give queryset after parsing it.'''
    value = request.QUERY_PARAMS.get(param, None)
    if value:
        try:
            return arrow.get(value).datetime
        except arrow.parser.ParserError:
            return None
    return None
