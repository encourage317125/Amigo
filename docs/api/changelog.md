<style>
    .container h1{font-size: 1.5em; }
    .container h2{font-size: 1.2em; }
    .container hr{margin-top: 5px; }
</style>

# 2.2.0
## 2016-09-13

- Implemented cancel event API
- Expose `has_seen` field for GET event detail API

## 2016-08-16

- brand new UX released
- implemented randomized sample sent/received events
- add POST /users/register_fb_token API
- add GET /users/fb_friends API


## 2015-08-03

- add `/events/timeline` endpoint.
- remove `/users/invite_to_amigo` endpoint.
- remove all `/phonebooks` endpoints.
- add `GET`, `POST`, `DELETE` for `/users/favorite_contacts`.
- update the response format of `POST /users/from_phone_numbers`.


## 2015-08-01
- add `POST /auth/verify_pin` endpoint
- `POST /auth` no longer returns any user data.

# 2.0.0

## 2015-07-29

- replace `/events` with `/events-v2` endpoint
- implement the logic to consider events with `is_time_specified` into unresponded events. (#114)

## 2015-07-23

- update copy of invite to event sms.
- add `/events-v2` endpoint

## 2015-07-22

- auto invite to amigo when a phone_number is marked as favorite (#116)
- add copy for event venue removed notification

## 2015-07-16

- add new push notification, when `spots_left` decreased to 1 (#69)

## 2015-07-14

- add `notify_event_full` and `notify_upcoming_event` in user object.
- add new push notification: total spots increased for a event 
- remove `notify_event_change` and `notify_invite_change` from user object.

## 2015-07-13

- add/remove favorite contacts in my phonebook (#96)
- update `phonebooks/bulk_add_update_contacts` endpoint to just `bulk_add_contacts` and drop `full_name` from Phonebook Contact object (#94)

## 2015-07-10

- add `/remove_ios_device` endoint
- add `/events/stats` endoint, that return `unresponded_invite_count`

## 2015-07-08

- add `notify_contact_joined` property to `User` object.

## 2015-07-06

- return associated `user` for each of contact item based on matching phone_number

## 2015-07-02

- add `delete_others` parameter to `/phonebooks/bulk_add_or_update_contacts`
- update `/phonebooks/bulk_add_or_update_contacts` to return refreshed data in response

## 2015-07-01

- modify `/phonebooks/bulk_add_or_update_contacts` to accept `data` as property instead of sending all contacts as array at top-level

## 2015-06-29

- add `GET /phonebooks/contacts` endpoint
- add `POST /phonebooks/bulk_add_or_update_contacts` endpoint

## 2015-06-25

- add `i_am_filter` filter in `/events` endpoint

## 2015-06-16

- add `venue_name` property to Event resource
- add `users/invite_to_amigo` endpoint

## 2015-06-11

- add `rsvp_time` to list of invitees in Event detail resource


## 2015-06-10

- add `invitees_photos` to `GET /events`

## 2015-06-08

- add `location` and `address` to `Event` resource

## 2015-05-29

- remove automatically adding event_owner to attendee/invitee list.
- add `created` property to invitees resource.
- rename `spots_available` to `total_spots` for `Event` Resource.
- make `photo` & `big_photo` as `null` when no photo is upload by user.

## 2015-05-28

- add `my_rsvp_message` property to `Event` object
- add `is_time_specified` property to `Event` resource, to indicate whether "event_date" contains a accurate time of day or not.

## 2015-05-27

- rename `/events/:id/unaccept` to `/events/:id/reject` (better semantics)

## 2015-05-25

- make `i_am_attending` nullable to indicate that user has yet to responded to the invitation.
- add `rsvp_message` parameter to `POST /events/:id/accept` & `POST /events/:id/accept` and the same is returned at `GET /events/:id`

---

# 1.5.0

## 2014-01-31

- add endpoint `GET` `/users/who_has_invited_me`

# 1.4.0

----

## 2014-01-26

- add ability to unattend an event [`POST`] `/events/:id/unaccept`

# 1.3.0

----

## 2014-01-13

- add user preference `notify_event_change`, which defaults to `true`
- event invitees will have `is_owner`, `photo` & `big_photo` in it. Photo url will be present only if invitee is registered amigo user.

## 2014-01-05

- add endpoints `/users/change-avatar` and `/users/remove-avatar`
- `User` object will now have  `photo` and `big_photo` properties

## 2014-01-04

- `/events` can now be filter based on `event_date` using the querystring `?event_after` and `?event_before`. These parameter accepts unix timestamp or ISO-8601 string

## 2014-01-24

- Following new fields are added to `User` to store notification preferece: `notify_new_invite`, `notify_invite_change`, `notify_invite_rsvp`

## 2014-01-24

- add `notifications/add_ios_device`
- `Event` object will now have `attendees_count` property


# 1.0.0

## 2014-09-20

- add implementation for `/events/:id/mark_seen`
- add implementation for `/events/:id/accept`
- `Event` object will now have a `i_have_seen` property

## 2014-09-17

- add information on how to modify event object, including inviting more users, update filled spots, available spots.

## 2014-09-16

- add `invitees_count` in all the event view. Remove `invitees` object from events list (`/events`)

## 2014-09-14

- add implementaton of `/users/from_phone_numebrs`
- remove `full_name_display`
- Add full `owner` object to `Event`
- `Event` object will now have `i_am_attending` property
- `Event` object will now have `invitees` instead of `attendees`

## 2014-09-13

- `Event` object will now have `i_am_owner` instead of full `owner` object

## 2014-09-10

- rename auth endpoint from `/login` to `/auth`
- add `/auth/register` endpoint
- `is_new` is replaced with `is_active`

## 2014-09-8

- Use `full_name` instead of `name` for user 
