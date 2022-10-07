# Third Party Stuff
from django.contrib import admin

from . import models


@admin.register(models.SampleRSVPReply)
class SampleRSVPMessageAdmin(admin.ModelAdmin):
    list_display = ('text', 'type', 'created', 'modified')
    list_filter = ('type', 'created', 'modified')
    search_fields = ('type', 'text')


@admin.register(models.Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'attendees_count', 'owner',
                    'event_date', 'created', 'modified', 'invitees_list')
    list_display_links = ('id', 'title', )
    list_filter = ('event_date', 'created', 'modified')
    search_fields = ('title', 'venue_name')


@admin.register(models.SampleEvent)
class SampleEventAdmin(admin.ModelAdmin):
    list_display = ('type', 'title', 'venue_name', 'address', 'city',
                    'event_date', 'created', 'modified')
    list_display_links = ('title', )
    list_filter = ('type', 'event_date', 'city', 'created')
    search_fields = ('title', 'city', 'venue_name')


@admin.register(models.Invitation)
class InvitationAdmin(admin.ModelAdmin):
    list_display = ('id', 'event', 'user', 'phone_number', 'invited_by', 'has_accepted_invite', 'created',)
    list_display_links = ('id', 'event', )
    list_filter = ('user', 'event', 'created',)
    search_fields = ('event__title', 'event__venue_name', 'user__full_name', )


@admin.register(models.InviteText)
class InviteTextAdmin(admin.ModelAdmin):
    list_display = ('invite_text',)
    list_display_links = ('invite_text',)
    list_filter = ()
    search_fields = ('invite_text',)
