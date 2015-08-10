from django.contrib import admin

from .models import Queue, Sla, Status, Ticket, Break


class QueueAdmin(admin.ModelAdmin):

    list_display = ("title", )


class SlaAdmin(admin.ModelAdmin):

    list_display = ("service", "queue", "days_budget", "days_delivery", "value")
    list_filter = ("queue", )


class StatusAdmin(admin.ModelAdmin):

    list_display = ("ticket", "added")


class TicketAdmin(admin.ModelAdmin):

    search_fields = ("identifier", "title")
    list_display = ("identifier", "title", "start_date", "end_date", "sla")
    # list_filter = ("status", )


class BreakAdmin(admin.ModelAdmin):

    list_display = ("ticket", "date", "reason")
    # list_filter = ("status", )


admin.site.register(Queue, QueueAdmin)
admin.site.register(Sla, SlaAdmin)
admin.site.register(Status, StatusAdmin)
admin.site.register(Ticket, TicketAdmin)
admin.site.register(Break, BreakAdmin)
