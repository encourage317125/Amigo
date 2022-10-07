# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

# Third Party Stuff
from django.contrib import admin
from django.contrib.auth.models import Group
from django.db.models import IntegerField
from django.db.models import Count, Sum, Case, When

from . import models
from .forms import UserCreationForm


class UserAdmin(admin.ModelAdmin):
    # def queryset(self, request):
    #     qs = models.User.objects.annotate(invited_count=Count('invitations'))
    #     qs = qs.extra({
    #         'attended_invitees': '(SELECT COUNT(ei.id) \
    #          FROM events_invitation ei WHERE ei.user_id = users_user.id \
    #          AND ei.has_accepted_invite = true)',
    #         'average_invite_count': '(SELECT \
    #             (SELECT COUNT(ei.id) FROM events_invitation ei \
    #              WHERE ei.event_id IN (SELECT ee.id FROM events_event ee \
    #                 WHERE ee.owner_id = users_user.id)) \
    #             / NULLIF(COUNT(ee.id), 0) FROM events_event ee \
    #             WHERE ee.owner_id = users_user.id)',
    #     })
    #     return qs
    def uniq_inv(self, obj):
        return obj.uniq_inv
    uniq_inv.short_description = 'Unique Invitees'
    uniq_inv.admin_order_field = 'uniq_inv'

    def total_app(self, obj):
        return obj.total_app
    total_app.short_description = 'Total App Invitees'
    total_app.admin_order_field = 'total_app'

    def total_passive(self, obj):
        return obj.total_passive
    total_passive.short_description = 'Total Passive Invitees'
    total_passive.admin_order_field = 'total_passive'

    def total_inactive(self, obj):
        return obj.total_inactive
    total_inactive.short_description = 'Total Inactive Invitees'
    total_inactive.admin_order_field = 'total_inactive'

    def get_queryset(self, request):
        qs = super(UserAdmin, self).get_queryset(request)
        qs = qs.annotate(uniq_inv=Count('ihaveinvited__user', distinct=True),
                         total_app=Sum(
                                        Case(
                                            When(ihaveinvited__invitee_current_status=0, then=1),
                                            default=0,
                                            output_field=IntegerField()
                                        )
                                    ),
                         total_passive=Sum(
                                        Case(
                                            When(ihaveinvited__invitee_current_status=1, then=1),
                                            default=0,
                                            output_field=IntegerField()
                                        )
                                    ),
                         total_inactive=Sum(
                                        Case(
                                            When(ihaveinvited__invitee_current_status=2, then=1),
                                            default=0,
                                            output_field=IntegerField()
                                        )
                                    ),
                         )
        return qs

    def average_invite_count(self, obj):
        """
        Returns the count of created events.
        """
        return obj.average_invite_count
    average_invite_count.short_description = 'Created events'
    average_invite_count.admin_order_field = 'average_invite_count'

    def number_attended_events(self, obj):
        """
        Returns the number of invited and attended events.
        """
        return "{}/{}".format(obj.attended_invitees, obj.invited_count)
    number_attended_events.short_description = 'Attended events / Invited'
    number_attended_events.admin_order_field = 'attended_invitees'

    model = models.User
    add_form = UserCreationForm
    list_display = ('phone_number', 'email', 'full_name', 'is_active',
                    'date_joined', 'last_login',
                    'is_app_user', 'uniq_inv', 'total_app', 'total_passive',
                    'total_inactive',)
    list_filter = ('is_superuser', 'is_active',)
    search_fields = ('phone_number', 'full_name', 'email',)
    ordering = ('last_login',)


admin.site.register(models.User, UserAdmin)
admin.site.unregister(Group)
