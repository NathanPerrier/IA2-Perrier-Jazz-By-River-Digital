from ..config import *

class PaymentStatusAdmin(admin.ModelAdmin):
    list_display = ('id', 'status', 'status_code', 'last_modified')
    search_fields = ('id', 'status', 'last_modified')