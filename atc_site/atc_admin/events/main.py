from ..config import *

class EventsAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'location', 'date', 'time', 'available_tickets', 'sold', 'sale_release_date', 'sale_end_date', 'creation_time', 'last_modified', 'organizer', 'ticket_price', 'image')
    search_fields = ('name', 'description', 'location', 'date', 'time', 'available_tickets', 'sold', 'sale_release_date', 'sale_end_date', 'creation_time', 'last_modified', 'organizer', 'ticket_price', 'image')
    
