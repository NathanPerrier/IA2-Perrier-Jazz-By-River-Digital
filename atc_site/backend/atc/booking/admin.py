"""Admin classes for the booking app."""
from django.contrib import admin

from modeltranslation.admin import TranslationAdmin

from . import models

class BookingStatusAdmin(TranslationAdmin):
    list_display = ['slug', 'name']

class BookingAdmin(admin.ModelAdmin):
    list_display = [
        'creation_date', 'booking_status', 'booking_id', 'user', 'email',
        'session', 'date_from', 'date_until',
    ]


class BookingItemAdmin(admin.ModelAdmin):
    list_display = ['booking', 'booked_item', 'quantity', 'persons']

admin.site.register(models.Booking)
admin.site.register(models.BookingError)
admin.site.register(models.BookingItem)
admin.site.register(models.BookingStatus, BookingStatusAdmin)  # Use the custom admin class here
admin.site.register(models.ExtraPersonInfo)
# admin.site.register(models.Booking, BookingAdmin)
# admin.site.register(models.BookingError)
# admin.site.register(models.BookingItem, BookingItemAdmin)
# admin.site.register(models.BookingStatus, TranslatableAdmin)
# admin.site.register(models.ExtraPersonInfo)
