from ..config import *

class LocationImagesModelAdmin(admin.ModelAdmin):
    list_display = ('location', 'image')
    search_fields = ('location', 'image')