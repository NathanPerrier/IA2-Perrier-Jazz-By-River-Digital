from ..config import *

class EventScheduleAdmin(admin.ModelAdmin):
    list_display = ('event', 'event_item')
    search_fields = ('event', 'event_item')