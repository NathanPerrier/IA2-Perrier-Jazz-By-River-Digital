from ..config import *

class EventVoucherAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('name', 'description', 'event')
    search_fields = ('name', 'description')