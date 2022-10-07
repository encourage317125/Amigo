Different push notifications sent out to iOS and there payload.

# Invited to Event

As a user, when an event creator invites me to an event, I receive a push notification.

This notification type is listed in notification settings as “I receive a message”.

```
{
    "aps": {
        "alert": "[EVENT CREATOR] invited you to: [MESSAGE COPY]."
    },
    "event_id": {{event.id}},
    "type": "invite",
    "title": "{{event.title}}"
}
```

# Event Reminder

As an attendee, when an event with a set date/time is 24 hours away, I want to receive a push notification.

```
{
    "aps": {
        "alert": "[EVENT MESSAGE] is happening tomorrow!"
    },
    "event_id": {{event.id}},
    "type": "reminder",
    "title": "{{event.title}}"
}
```

# RSVP - Attending

As an event creator, when someone accepts my invite I receive a push notification.

This notification type is listed in notifications settings as “When an Amigo accepts my invite”.

- Copy: “[NAME] responded with: [ACCEPT RESPONSE]. Down to [AMOUNT OF OPEN SPOTS] spots.”
- Copy: “[NAME] responded with: [ACCEPT RESPONSE]. Down to 1 spot. Sweet.”

```
{
    "aps": {
        "alert": "[NAME]: [ACCEPT RESPONSE]. Down to [AMOUNT OF OPEN SPOTS] spots."
    },
    "event_id": {{event.id}},
    "type": "rsvp",
    "title": "{{event.title}}"
}
```

# RSVP - Unattending

When a user un-accepts the invitation, the event owner gets a notification.

```
{
    "aps": {
        "alert": "[USER] can no longer make it. [NUMBER OF SPOTS LEFT] spots left."
    },
    "event_id": {{event.id}},
    "type": "rsvp",
    "title": "{{event.title}}"
}
```

# Event Change

## Event Message(title) Change

As an attendee, when an event creator changes the message of an event I am attending, I want to receive a notification updated.

```
{
    "aps": {
        "alert": "[EVENT CREATOR] has changed [OLD EVENT MESSAGE] to [NEW EVENT MESSAGE]."
    },
    "event_id": {{event.id}},
    "type": "change",
    "title": "{{event.title}}"
}
```

## Event Time Change

As an attendee, when an event creator changes the time of an event I am attending, I want to receive a notification update.

```
{
    "aps": {
        "alert": "{{event_owner}} has changed the time of {{event_title}}."
    },
    "event_id": {{event.id}},
    "type": "change",
    "title": "{{event.title}}"
}
```

## Event Location Change

As an attendee, when an event creator changes the location of an event I am attending, I want to receive a notification update.

- copy: Heads up! [event_owner] has removed the location of [event_title].
- copy: Heads up! [EVENT CREATOR] has changed the location of [EVENT MESSAGE] to [VENUE TITLE].

```
{
    "aps": {
        "alert": "Heads up! [EVENT CREATOR] has changed the location of [EVENT MESSAGE] to [VENUE TITLE]."
    },
    "event_id": {{event.id}},
    "type": "change",
    "title": "{{event.title}}"
}
```

## Event Spots Change (Increase)

As an invitee, when an event creator increases the amount of spots to an event that was previously full, I want to receive a notification update.

```
{
    "aps": {
        "alert": "[EVENT CREATOR] has added spots for [EVENT MESSAGE]. Get in there!"
    },
    "event_id": {event.id},
    "type": "change",
    "title": "{event.title}"
}
```

## Spots left decreased to 1 for a event 

As an invitee, when an event creator decreases the amount of spots to an event so that only 1 open spot remains, I want to receive a notification update. 

> Note: This push is never for events with only one available spot. If the event is created with 1 open spot, the creator would have to add a second spot and then receive an RSVP for this push to be sent to remaining users.

As an invitee, when a new attendee(s) causes remaining spots of an event to decrease to 1, I want to receive a notification update.

In both of these scenarios, only invitees who have been invited, but not yet replied should receive the push notification.

```
{
    "aps": {
        "alert": "[EVENT CREATOR]: [MESSAGE COPY]. Get the last spot!"
    },
    "event_id": {event.id},
    "type": "change",
    "title": "{event.title}"
}
```

## Event is Full

As an event creator, when the last open spot on your event is filled you receive a push notification. 

This notification type is listed in notification settings as “My sent event is full”.

- copy: “[NAME] is joining you. Have fun you two!”
- copy: Your amigos have filled all [AMOUNT OF TOTAL SPOTS] spots for your event. Have a blast!

```
{
    "aps": {
        "alert": "Your amigos have filled all [AMOUNT OF TOTAL SPOTS] spots for your event. Have a blast!"
    },
    "event_id": {event.id},
    "type": "change",
    "title": "{event.title}"
}
```

# Contact Joins Amigo

As a user, when a contact from my address book joins (registers on) Amigo, I receive a push notification. 

This notification type is listed in notifications setting as “One of my contacts joins Amigo”.

```
{
    "aps": {
        "alert": "[CONTACT NAME] just joined Amigo. Now you can hang out in a heartbeat!"
    },
    "user_id": {{user.id}},
    "type": "new_user",
}
```

---

# SMS Notification

## Invitation to Join

As a user without Amigo, when an Amigo user invites me to join Amigo, I receive a text message.

> “[SENDER NAME] is using Amigo to make it easier to get together with friends and thinks you should join too! Get the app here: [APP STORE LINK].”

## Invitation to Event

> “You’re invited! [EVENT CREATOR] wants you to join for [EVENT MESSAGE]. Please RSVP on Amigo: [APP STORE LINK].”
