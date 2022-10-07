# Third Party Stuff
from django.contrib import admin

from . import models


@admin.register(models.EventToken)
class EventToken(admin.ModelAdmin):
    list_display = ('token', 'user', 'used_at', 'event')
    list_filter = ('token', 'user', 'used_at', 'event')
    search_fields = ('token',)
