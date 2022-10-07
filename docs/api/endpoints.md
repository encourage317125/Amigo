For api overview and usages, check out [this page](overview.md).

[TOC]

# Authentication

## Login

```
POST /auth
```

__Parameters__

Name         | Type    | Description
-------------|---------|---------------------------------------------
phone_number | string  | Standard phone number, must include (+)

__Example__

```
{
  "phone_number": "+98787676767"
}
```

__Response__

`204 No Content`

## Verify phone

```
POST /auth/verify_pin
```

__Parameters__

Name         | Type    | Description
-------------|---------|---------------------------------------------
phone_number | string  | Standard phone number, must include (+)
pin          | string  | The pin that is been sent to the user (through text message)

__Response__
```json
{
    "id": 1,
    "is_active": true,
    "full_name": "John Doe",
    "photo": "http://theserver.com/default.jpeg?size=80",
    "big_photo": "http://theserver.com/default.jpeg?size=300",
    "email": "john@example.com",
    "notify_new_invite": true,
    "notify_invite_rsvp": true,
    "notify_contact_joined": true,
    "notify_event_full": true,
    "notify_upcoming_event": true,
    "phone_number": "+98787676767",
    "auth_token": "aslkdfjalskdfjasdkfasdf7a86*&^87234sdfasdf"
}
```

`400 BAD REQUEST` when pin is not correct.

## Register

```
POST /auth/register (requires authorization)
```

__Parameters__

Name         | Type    | Description
-------------|---------|---------------------------------------------
full_name    | string  | min. 2 chars and max. 256 characters
email        | string  | valid email address, max length 256 chars

__Response__

```json
{
    "id": 1,
    "is_active": true,
    "full_name": "John Doe",
    "photo": "http://theserver.com/default.jpeg?size=80",
    "big_photo": "http://theserver.com/default.jpeg?size=300",
    "email": "john@example.com",
    "notify_new_invite": true,
    "notify_invite_rsvp": true,
    "notify_contact_joined": true,
    "notify_event_full": true,
    "notify_upcoming_event": true,
    "phone_number": "+98787676767",
    "auth_token": "aslkdfjalskdfjasdkfasdf7a86*&^87234sdfasdf"
}
```

## Register/Deregister iOS device

```
POST /notifications/add_ios_device  (requires authorization)
POST /notifications/remove_ios_device  (requires authorization)
```

__Parameters__

Name         | Type    | Description
-------------|---------|---------------------------------------------
token        | string  | 64 charater long apple device token

__Example__

    {
        "token": <64_digit_device_token>
    }

## Register Facebook Token

```
POST /users/fb_token (requires authorization)
```

__Parameters__

Name         | Type    | Description
-------------|---------|---------------------------------------------
fb_token     | string  | A valid, non expired Access Token issued from [Facebook Graph API](https://developers.facebook.com/docs/graph-api)

__Response__

```json
{
  "id": 22,
  "phone_number": "+14155558888",
  "full_name": "Amigo Gonzales",
  "email": "wei@amigo.io",
  "is_active": true,
  "notify_new_invite": true,
  "notify_invite_rsvp": true,
  "photo": "http://localhost:8000/media/_s_/users/user/2PTAk2hxRx66IwSse5fS9A-crop-c0-5__0-5-60x60.jpg",
  "big_photo": "http://localhost:8000/media/_s_/users/user/2PTAk2hxRx66IwSse5fS9A-crop-c0-5__0-5-250x250.jpg",
  "notify_contact_joined": true,
  "notify_event_full": true,
  "notify_upcoming_event": true
}
```

## Change/remove user avatar

```
POST /users/change_avatar (requires authorization)
```

__parameters__

Name         | Type    | Description
-------------|---------|---------------------------------------------
photo        | image   | Only jpeg and png are supported

__NOTE__: use `multipart/form-data` as request format

__Response__

    {
        "id": 1,
        "is_active": true,
        "full_name": "John Doe",
        "photo": "https://theserver.com/realimage.jpeg?size=80",
        "big_photo": "https://theserver.com/realimage.jpeg?size=300",
        "email": "john@example.com",
        "notify_new_invite": true,
        "notify_invite_rsvp": true,
        "notify_contact_joined": true,
        "notify_event_full": true,
        "notify_upcoming_event": true,
        "phone_number": "+98787676767",
    }

To remove user avatar, send an empty `POST` request at:

```
POST /users/remove_avatar (requires authorization)
```


---

# Events

## Get all events

```
GET /events (requires authorization)
```

This endpoint will return a paginated list of all the events the authorized user has either created or been invited to.

To filter the events based on `event_date`, you can pass the following querystring `?event_after` & `?event_before`. The value can be [UNIX timestamp](http://en.wikipedia.org/wiki/Unix_time) or ISO-8601 compliant string.

e.g 
```
/events?event_after=1415101887
/events?event_before=1415104887
/events?event_after=1415101887&event_before=1415104887
```

To get only events created by requesting user, use `i_am_owner` filter. 

e.g:
```
/events?i_am_owner=true
/events?i_am_owner=false
```

__Response__

    {
        count: 30,
        next: "http://example.com/events/page=2",
        previous: null,
        results: [{
            "id": 78,
            "title": "Dinner @ Street4",
            "event_date": "2014-03-12T12:30+5:30",
            "is_time_specified": true,
            "created": "2014-03-11T12:30+5:30",
            "modified": "2014-03-11T12:30+5:30",
            "total_spots": 2,
            "spots_filled": 0,
            "i_am_owner": True,
            "i_am_attending": True,
            "location": {},
            "address": "",
            "venue_name": "",
            "owner": {
                "id": 1,
                "is_active": true,
                "full_name": "John Doe",
                "email": "john@example.com",
                "phone_number": "+98787676767",
                ...
            }
        }, {
            "id": 78,
            "title": "Dinner @ Street4",
            "event_date": "2014-03-12T00:00+5:30",
            "is_time_specified": false,
            "created": "2014-03-11T12:30+5:30",
            "modified": "2014-03-11T12:30+5:30",
            "total_spots": 2,
            "spots_filled": 0,
            "i_am_owner": True,
            "i_am_attending": False,
            "location": {},
            "address": "",
            "venue_name": "",
            "owner": {
                "id": 1,
                "is_active": true,
                "full_name": "John Doe",
                "email": "john@example.com",
                "phone_number": "+98787676767",
                ...
            }
        },
        ...
        ]
    }

## Event timeline


```
GET /events/timeline (requires authorization)
```

__Parameter__

Name              | Type    | Description
------------------|---------|---------------------------------------------
type        | string  | (required) possible values are `sent` and `received`
cursor            | string  | `event_date` of last item in the result. Use for fetch the next page of result. The result ends when there are not results.

e.g:
```
/events/timeline?type=sent
/events/timeline?type=received
```

or, to fetch the next page

```
/events/timeline?type=sent&cursor=2015-08-03T13:11:47.357035Z
/events/timeline?type=received&cursor=2015-08-03T13:11:47.357035Z
```

__Response__

```
[
  {
    "id": 5,
    "title": "Dinner @ my place",
    "event_date": "2015-08-05T11:38:51.036976Z",
    "created": "2015-08-05T11:38:51.097753Z",
    "modified": "2015-08-05T11:38:51.099447Z",
    "owner": {
      "id": 4,
      "phone_number": "+918377080003",
      "full_name": "User 3",
      "email": "user0003@email.com",
      "is_active": true,
      "notify_new_invite": true,
      "notify_invite_rsvp": true,
      "photo": "http://localhost:8000/media/_s_/users/user/uC0_vVJoR9G7BWCQ1rCprg-crop-c0-5__0-5-60x60.jpg",
      "big_photo": "http://localhost:8000/media/_s_/users/user/uC0_vVJoR9G7BWCQ1rCprg-crop-c0-5__0-5-250x250.jpg",
      "notify_contact_joined": true,
      "notify_event_full": true,
      "notify_upcoming_event": true
    },
    "total_spots": 20,
    "spots_filled": 0,
    "i_am_owner": true,
    "i_am_attending": true,
    "is_time_specified": true,
    "location": {},
    "address": "",
    "venue_name": "",
    "my_rsvp_message": null,
    "invitees": [
      {
        "id": 0,
        "full_name": "",
        "phone_number": "+9000920234234",
        "is_attending": null,
        "is_active": false,
        "is_owner": false,
        "photo": "https://example.com/60x60.jpg",
        "big_photo": "https://example.com/250x250.jpg",
        "faded_photo": "https://example.com/faded/60x60.jpg",
        "rsvp_message": null,
        "rsvp_time": null,
        "created": "2015-08-05T11:38:51.108776Z"
      }
    ]
  },
  {
    "id": 2,
    "title": "Event 1",
    "event_date": "2015-08-03T13:11:47.357035Z",
    "created": "2015-08-03T12:11:47.541346Z",
    "modified": "2015-08-03T12:11:47.544153Z",
    "owner": {
      "id": 1,
      "phone_number": "+918377080000",
      "full_name": "User 0",
      "email": "user0000@email.com",
      "is_active": true,
      "notify_new_invite": true,
      "notify_invite_rsvp": true,
      "photo": "http://localhost:8000/media/_s_/users/user/iuVx7d2FQimh5fcUP8yoPw-crop-c0-5__0-5-60x60.jpg",
      "big_photo": "http://localhost:8000/media/_s_/users/user/iuVx7d2FQimh5fcUP8yoPw-crop-c0-5__0-5-250x250.jpg",
      "notify_contact_joined": true,
      "notify_event_full": true,
      "notify_upcoming_event": true
    },
    "total_spots": 72,
    "spots_filled": 10,
    "i_am_owner": true,
    "i_am_attending": true,
    "is_time_specified": true,
    "location": {},
    "address": "",
    "venue_name": "",
    "my_rsvp_message": null,
    "invitees": []
  }
]
```

## Create new event

```
POST /events (Requires authorization)
```

__Parameters__

Name              | Type    | Description
------------------|---------|---------------------------------------------
title             | string  | Name of the event, max 200 chars
event_date        | string  | time of event in ISO8601 format, if user doesn't select the time, put time part as `00:00` and make `is_time_specified` property as `true`
is_time_specified | boolean | Whether time is specified by user while creating the event
total_spots       | number  | Number of available spots, this is independent of invited users.
invite_phone_numbers | array | Array of phone numbers in standard format
location          | json    | (optional) json in the format `{"latitude": 12, "longitude": 12.3}`
address           | string  | (optional) full address of the event.
venue_name        | string  | (optional) max. length 100

__Example__

    {
        "title": "Dinner @ my place",
        "event_date": "2014-10-15T12:51:40+0000",
        "is_time_specified": true,
        "total_spots": 20,
        "invite_phone_numbers": ["+9000920234234", "+1235550011"],
        "location": {"latitude": 23.4, "longitude": 89.8},
        "address": "568 Broadway, 11th fl. \nNew York, NY 10012",
        "venue_name": "Amigo Office"
    }

__Response__

```
{
  "id": 4,
  "title": "Dinner @ my place",
  "event_date": "2014-10-15T12:51:40+0000",
  "is_time_specified": true,
  "created": "2014-10-15T12:51:40+0000",
  "modified": "2014-10-15T12:51:40+0000",
  "owner": {
    "id": 13,
    "phone_number": "+1235550010",
    "full_name": "User 10",
    "email": "user0010@email.com",
    "is_active": true
  },
  "total_spots": 20,
  "spots_filled": 0,
  "i_am_owner": true,
  "i_am_attending": true,
  "my_rsvp_message": null,
  "attendees_count": 0,
  "location": {"latitude": 23.4, "longitude": 89.8},
  "address": "568 Broadway, 11th fl. \nNew York, NY 10012",
  "venue_name": "Amigo Office",
  "invitees": [
    {
      "id": 10,
      "full_name": "User 5",
      "phone_number": "+1235550005",
      "is_attending": "True",
      "is_active": true,
      "is_owner": true,
      "photo": "http://example.com/_s_/100x100/image.jpg",
      "big_photo": "http://example.com/_s_/300x300/image.jpg",
      "rsvp_message": null,
      "rsvp_time": null,
      "created": "2014-10-15T12:51:40+0000"
    },
    {
      "id": 11,
      "full_name": "User 6",
      "phone_number": "+1235550006",
      "is_attending": null,
      "is_active": true,
      "is_owner": false,
      "photo": "http://example.com/_s_/100x100/image.jpg",
      "big_photo": "http://example.com/_s_/300x300/image.jpg",
      "rsvp_message": "I'll be there!",
      "rsvp_time": "2014-11-15T12:51:40+0000",
      "created": "2014-10-15T12:51:40+0000"
    }
  ]
}
```

## Get event details

```
GET /events/:id
```

__Response__
```
{
  "id": 4,
  "title": "Dinner @ my place",
  "event_date": "2014-10-15T12:51:40+0000",
  "created": "2014-10-15T12:51:40+0000",
  "modified": "2014-10-15T12:51:40+0000",
  "owner": {
    "id": 13,
    "phone_number": "+1235550010",
    "full_name": "User 10",
    "email": "user0010@email.com",
    "is_active": true
  },
  "total_spots": 20,
  "spots_filled": 0,
  "i_am_owner": true,
  "i_am_attending": true,
  "my_rsvp_message": null,
  "location": {"latitude": 23.4, "longitude": 89.8},
  "address": "568 Broadway, 11th fl. \nNew York, NY 10012",
  "venue_name": "Amigo Office",
  "invitees": [
    {
      "id": 10,
      "full_name": "User 5",
      "phone_number": "+1235550005",
      "is_attending": "True",
      "is_active": true,
      "is_owner": true,
      "has_seen": true,
      "photo": "http://example.com/_s_/100x100/image.jpg",
      "big_photo": "http://example.com/_s_/300x300/image.jpg",
      "rsvp_message": null,
      "rsvp_time": null,
      "created": "2014-10-15T12:51:40+0000"
    },
    {
      "id": 11,
      "full_name": "User 6",
      "phone_number": "+1235550006",
      "is_attending": null,
      "is_active": true,
      "is_owner": false,
      "has_seen": false,
      "photo": "http://example.com/_s_/100x100/image.jpg",
      "big_photo": "http://example.com/_s_/300x300/image.jpg",
      "rsvp_message": null,
      "rsvp_time": null,
      "created": "2014-10-15T12:51:40+0000"
    }
  ]
}
```

## Cancel event

```
PUT /events/:id/cancel_event
```

__Response__
```
204 No Content
```

## Get unresonded invites count

Returns count of invites that are upcoming, received, Unresponded and are non-expired. 

```
GET /events/stats
```

__Response:__

```
{
  "unresponded_invite_count": 3
}
```


## Invite users

```
PATCH /events/:id  (Requires authorization)
```

__Parameters__

- `invite_phone_numbers` - array of phone numbers in standard format

__Example__

    {
        "invite_phone_numbers": ["+9000920234234", "+1235550011"]
    }

__Response__

Response will be updated full `Event` object.

## Get list of possible rsvp reply messages

```
GET /events/sample_rsvp_replies (Authentication required)
```

__Response__
```
[
  {
    "id": 3,
    "text": "Maybe next time!",
    "type": "reject"
  },
  {
    "id": 1,
    "text": "I'll be there :)",
    "type": "accept"
  },
  {
    "id": 2,
    "text": "Yesss!",
    "type": "accept"
  }
]
```

Note: this endpoint will not be paginated

## Accept an invitation

```
POST /events/:id/accept (Requires authorization)
```

Name           | Type       | Description
---------------|------------|---------------------------------------------
rsvp_message   | string     | (optional) message sent by user while replying to an event. max. length=60)


## Reject an invitation

```
POST /events/:id/reject (Requires authorization)
```

Name           | Type       | Description
---------------|------------|---------------------------------------------
rsvp_message   | string     | (optional) message sent by user while replying to an event. max. length=60)


## Mark an invitation as seen

```
POST /events/:id/mark_seen (Requires authorization)
```

No parameter required, just send an empty `POST` call at this endpoint.

## Fill Spots

```
PATCH /events/:id (Requires authorization)
```

__Parameters__

Name           | Type       | Description
---------------|------------|---------------------------------------------
spot_filled    | number     | numbers of spots to be filled

__Example__

    {
        "spot_filled": 90
    }

__Response__

Response will be updated full `Event` object.


---

# User

## Add/remove my phonebook contacts to favorite list

```
POST /users/favorite_contacts  (requires authorization)
DELETE /users/favorite_contacts  (requires authorization)
```


__Parameters__

Name           | Type     |  Description
---------------|--------- |---------------------------------------------
phone_numbers  | array    | phone numbers in standard format


__Example__
```
{
  "phone_numbers": ["+918456000001", "+918456000001" , "+918456000001"]
}
```

__Response__

```
Status: 200
```
```
{
  "success": True
}
```

## Get all your favorite contacts

```
GET /users/favorite_contacts
```


__Response__

```
[
  {
    "id": 8,
    "phone_number": "+918377080005",
    "is_favorite": True,
    "user": null
  },
  {
    "id": 6,
    "phone_number": "+918377080004",
    "is_favorite": True,
    "user": null
  },
  {
    "id": 5,
    "phone_number": "+918377080003",
    "is_favorite": True,
    "user": {
      "id": 4,
      "full_name": "User 3",
      "photo": "http://localhost:8000/media/_s_/users/user/fF9uk-jXT1egxueWQsO9yQ-crop-c0-5__0-5-60x60.jpg",
      "big_photo": "http://localhost:8000/media/_s_/users/user/fF9uk-jXT1egxueWQsO9yQ-crop-c0-5__0-5-250x250.jpg",
    }
  }
]
```


## Get users from phone numbers

This endpoints returns a list of users who are already registered on Amigo, for the given list of phone numbers.

```
POST /users/from_phone_numbers  (Requires authorization)
```

__Parameters__

Name           | Type       | Description
---------------|------------|---------------------------------------------
phone_numbers  | array      | standard international phone numbers including `+` 

__Example__

    {
      "phone_numbers": ["+918377080000", "+918377080001", "+14155553695"]
    }

__Note:__ This endpoint is not paginated.

__Response__

```
[
  {
    "phone_number": "+918377080000",
    "user": {
      "id": 1,
      "full_name": "User 0",
      "phone_number": "+918377080000",
      "photo": "http://examle.com/media/_s_/users/user/Sf0xhChLQ92w_tuEZK-wMw-crop-c0-5__0-5-60x60.jpg",
      "big_photo": "http://examle.com/media/_s_/users/user/Sf0xhChLQ92w_tuEZK-wMw-crop-c0-5__0-5-250x250.jpg",
    }
  }, {
    "phone_number": "+918377080001",
    "user": {
      "id": 2,
      "full_name": "User 1",
      "phone_number": "+918377080001",
      "photo": "http://examle.com/media/_s_/users/user/Sf0xhChLQ92w_tuEZK-wMw-crop-c0-5__0-5-60x60.jpg",
      "big_photo": "http://examle.com/media/_s_/users/user/Sf0xhChLQ92w_tuEZK-wMw-crop-c0-5__0-5-250x250.jpg",
    }
  }
]
```

## Get all the users who has invited me

This endpoints returns a list of users who are already registered on Amigo,
and has invited the user making request to any one event.

```
GET /users/who_has_invited_me
```

__Note:__ This endpoint is not paginated.

__Response__

    [
      {
        "id": 6,
        "phone_number": "+1235550007",
        "full_name": "User 7",
        "email": "user0007@email.com",
        "is_active": true,
        "notify_new_invite": true,
        "notify_invite_rsvp": true,
        "notify_event_change": true,
        "notify_contact_joined": true,
        "photo": "http://example.com/_s_/100x100/image.jpg",
        "big_photo": "http://example.com/_s_/300x300/image.jpg"
      }
    ]

## Get User's Facebook Friends

This endpoints returns a list of user's Facebook friends.

```
GET /users/fb_friends
```

__Response__

    [
        {
            "name": "Foo Bar",
            "id": "442506887580729"
        }
    ]
__Note:__ This endpoint is not paginated.
