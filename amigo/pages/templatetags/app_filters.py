# -*- coding: utf-8 -*-

from django import template
from datetime import datetime

register = template.Library()


@register.filter(name='firstFour')
def firstFour(data):
    return data[:4]


@register.filter(name='nextFive')
def newFive(data):
    return data[4:9]


@register.filter(name='friendly_timestamp')
def friendly_timestamp(timestamp):
    current_week_of_year = int(datetime.utcnow().strftime("%U"))
    target_week_of_year = int(timestamp.strftime("%U"))
    if target_week_of_year >= current_week_of_year:
        if target_week_of_year - current_week_of_year == 0:
            return 'This {}'.format(timestamp.strftime("%a %I:%M%p"))  # This Fri Mar 11 8:05PM
        elif target_week_of_year - current_week_of_year == 1:
            return 'Next {}'.format(timestamp.strftime("%a %b %d %I:%M%p"))  # Next Fri Mar 18 09:03PM
        else:
            return timestamp.strftime("%a %b %d %I:%M%p")
    return ''
