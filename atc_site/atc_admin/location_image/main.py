from ..config import *

class LocationImagesModelAdmin(admin.ModelAdmin):
    list_display = ('city', 'country', 'lat', 'lon', 'image_url', 'is_safe')
    search_fields = ('city', 'country', 'lat', 'lon', 'image_url', 'is_safe')