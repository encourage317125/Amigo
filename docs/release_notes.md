# Release Notes

## [2.2.0]

__Date:__ 2016-08-16

__Added__

- brand new UX released
- implemented randomized sample sent/received events
- add `POST` `/users/register_fb_token` API
- add `GET` `/users/fb_friends` API

## [2.1.0-dev]

__Date:__ [Unreleased](https://github.com/JoinAmigo/amigo-web/issues/133)

__Added__

- `faded_photo` to `/events/timeline` invitees objects
- `GET /events/timeline` endpoint
- `GET`, `POST`, `DELETE` for `/users/favorite_contacts`
- `POST /auth/verify_pin`

__Changed__

- Update the response format of `POST /users/from_phone_numbers`
- `/auth` reponse data.
- Upgrade to Django 1.8. (#147)

__Fixed__
- handle the case where two people are able to accept invite even all the spots are filled. (#143)

__Removed__

- all `/phonebooks` endpoints
- `/users/invite_to_amigo` endpoint.


## [2.0.0]

__Date:__ [31st July 2015](https://github.com/JoinAmigo/amigo-web/issues/38)

__Added__

- Mixpanel integration
- API Call for Badge Count (#90)
- API: add/update users' notification preferences (#37)
- Notification: Total spots changed for a event (#70)
- Notification: One Spot Left for Event (#69)
- Notification: upcoming event reminder (#103)
- Implement logout functionality (#89)
- Save/update users' phonebook on backend (#81)
- Update event notification change to be sent only attending users (#85)
- Notification: "One of your contact joined amigo" (#76)
- `invitees_photos` property to `GET /events` (#54)
- `rsvp_message` property to `POST /events/:id/accept` and `POST /events/:id/unaccept` (#34)
- `rsvp_message` to `invitees` array of object at `GET /events/:id` (#36)
- Optional `address` and `location` field to event object (#33)
- Database [persistent connections], for faster database access.
- `my_rsvp_message` property to `GET /events` and `GET /events/:id` (#45)
- `created` property to invitees resource so it can be sorted properly (#51)
- Api versioning support (followed by drf upgrade)
- `rsvp_time` in invitees for event detail (#58)
- `POST /users/invite_to_amigo` for inviting friends to amigo (#57)
- Add `venue_name` property to Event resource (#67)

__Changed__

- Implement/update new push notifications and sms messages (#65)
- Make time part in `event_date` optional by introducing `is_time_specified` property. (#46)
- Change `i_am_attending` property at `/events` resource nullable (#35)
- Rename `/events/:id/unaccept` to `/events/:id/reject` (#44)
- Upgrade to drf 3.0 (#43)
- For users without images, set image to null (#47)

[2.2.0]: https://github.com/JoinAmigo/amigo-web/compare/v2.2.0...master
[2.1.0-dev]: https://github.com/JoinAmigo/amigo-web/compare/v2.0.0...master
[2.0.0]: https://github.com/JoinAmigo/amigo-web/compare/v1.5.0...v2.0.0
