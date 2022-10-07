# -*- coding: utf-8 -*-
from __future__ import absolute_import
from django.conf import settings  # import the settings file

import datetime
import requests
import json
import hashlib
from datetime import timedelta
from icalendar import Calendar, vCalAddress, vText
from icalendar import Event as ICalendarEvent

from django.http import Http404, HttpResponse
from django.shortcuts import render

from amigo.notifications.models import EventToken
from amigo.events.services import mark_user_as_attending, mark_user_as_unattending
from autolink import linkify
from user_agents import parse
from validate_email import validate_email
from twilio.rest import TwilioRestClient
from twilio.rest.lookups import TwilioLookupsClient
from twilio.rest.exceptions import TwilioRestException
from HTMLParser import HTMLParser
import uservoice


def __validate_token(request):
    url_token = HttpResponse(request.GET.get('token')).content
    try:
        return EventToken.objects.get(token=url_token)
    except EventToken.DoesNotExist:
        raise Http404('Incorrect token')


def is_valid_number(number):
    client = TwilioLookupsClient()
    try:
        response = client.phone_numbers.get(number, include_carrier_info=True)
        response.phone_number  # If invalid, throws an exception.
        return True
    except TwilioRestException as e:
        if e.code == 20404:
            return False
        else:
            raise e


def invitation(request):
    token = __validate_token(request)
    parser = HTMLParser()

    ua_string = request.META['HTTP_USER_AGENT']
    user_agent = parse(ua_string)
    context = {}
    token.used_at = datetime.datetime.now()
    token.save()
    context['event'] = token.event
    context['formatted_title'] = parser.unescape(linkify(token.event.title, {'target': '_blank'}))
    event_attendees = []
    event_attendees.append(token.event.owner)
    if token.event.owner.id != token.user.id:
        event_attendees.append(token.user)
    for idx, invitee in enumerate(token.event.invitees.all()):
        if invitee.id == token.user.id or invitee.id == token.event.owner.id:
            continue
        event_attendees.append(invitee)
    context['event_attendees'] = event_attendees
    context['event_attendees_count'] = len(event_attendees)

    user = token.user

    if request.POST:
        if user.first_interaction is None:
            user.first_interaction = datetime.datetime.now()

        if request.POST['response'] == 'Accept':
            mark_user_as_attending(event=token.event, user=user,
                                   rsvp_message=request.POST['rsvp-message'])
        if request.POST['response'] == 'Decline':
            mark_user_as_unattending(event=token.event, user=user,
                                     rsvp_message=request.POST['rsvp-message'])

    if user_agent.os.family.lower() == 'ios':
        context['ios'] = True
        context['map_link'] = 'http://maps.apple.com/?q='
    else:
        context['ios'] = False
        context['map_link'] = 'http://maps.google.com/?q='

    context['is_pc'] = user_agent.is_pc
    return render(request, 'pages/invite.html', context)


def calendar(request):
    token = __validate_token(request)

    event = token.event
    cal = Calendar()
    cal.add('prodid', '-//Amigo INC//Event Calendar//EN')
    cal.add('version', '2.0')
    ic_evt = ICalendarEvent()
    ic_evt.add('summary', event.title)
    if event.venue_name:
        ic_evt.add('location', vText(event.venue_name))
    else:
        ic_evt.add('location', vText(event.address))

    ic_evt.add('dtstart', event.event_date)
    ic_evt.add('dtend', (event.event_date + timedelta(hours=1)))
    ic_evt.add('dtstamp', event.created)
    organizer = vCalAddress('MAILTO:{}'.format(event.owner.email))
    organizer.params['cn'] = vText(event.owner.full_name)
    ic_evt['organizer'] = organizer

    cal.add_component(ic_evt)
    # for attendee in event.attandes

    response = HttpResponse()
    response["Content-Type"] = "text/calendar"
    # response["Content-Disposition"] = "inline; filename={}-from-amigo.ics".format(event.title)
    response["Content-Disposition"] = "inline; filename=amigo.ics"
    response.write(cal.to_ical())
    return response


def send_email(request):
    subdomain_name = settings.USERVOICE_SUBDOMAIN_NAME
    api_key = settings.USERVOICE_API_KEY
    api_secret = settings.USERVOICE_API_SECRET
    client = uservoice.Client(subdomain_name, api_key, api_secret)

    response = HttpResponse()
    response["Content-Type"] = "text/html"
    # check response status

    email = request.POST['email']
    is_valid = validate_email(email)

    # Post a new ticket to your helpdesk from customer's email address
    if not is_valid:
        response.write('Invalid email')
        return response
    else:
        subject = request.POST['name']
        message = request.POST['message']
        question = client.post("/api/v1/tickets.json", {
            'email': email,
            'ticket': {
                'subject': subject,
                'message': message
            }
        })['ticket']

        if(question):
            response.write('1')
        else:
            response.write('0')
        return response


def send_sms(request):
    # check validity of toPhoneNo

    account_sid = settings.TWILIO_ACCOUNT_SID
    auth_token = settings.TWILIO_AUTH_TOKEN
    fromPhoneNo = settings.TWILIO_PHONE_NUMBER

    app_link_text = 'You can download app here: ' + 'https://itunes.apple.com/app/amigo/id1087152125'
    toPhoneNo = request.POST['number']

    response = HttpResponse()
    response["Content-Type"] = "text/html"
    # check response status
    if not is_valid_number(toPhoneNo):
        response.write('Invalid Phone Number')
        return response
    else:
        twilio_client = TwilioRestClient(account_sid, auth_token)

        message = twilio_client.messages.create(
            body=app_link_text,
            to=toPhoneNo,  # Customer's phone no
            from_=fromPhoneNo
        )  # our Twilio number

        if(message.sid):
            response.write('1')
        else:
            response.write('0')
        return response


def subscribe_mailchimp(request):
    response = HttpResponse()
    response["Content-Type"] = "text/html"
    # check response status

    email = request.POST['email']
    name = request.POST['name']
    is_valid = validate_email(email)
    if not is_valid:
        response.write('Invalid email')
        return response
    else:
        data = {
            'email_address': email,
            'status': "subscribed",
            'merge_fields': {
                    'FNAME': name,
                    'EMAIL': email}
                            }
        payload = json.dumps(data)
        memberid = hashlib.md5(email.lower()).hexdigest()

        url = "https://us11.api.mailchimp.com/3.0/lists/e09d426620/members/" + memberid
        headers = {
            'content-type': "application/json",
            'authorization': "Basic YW1pZ286MjdkMWFkNjM3YWUwYmZjZDljYTQ3NzU3NGQxMjkyYTktdXMxMQ==",
            'cache-control': "no-cache"
                  }

        myResponse = requests.request('PUT', url, data=payload, headers=headers)

        if(myResponse.ok):
            response.write('1')
        else:
            response.write('0')

        return response
