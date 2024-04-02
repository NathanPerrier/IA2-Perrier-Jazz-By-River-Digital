from ..config import *

class BookingStatusForm(forms.ModelForm):
    class Meta:
        model = BookingStatus
        fields = '__all__'
        
class BookingStatusAdmin(admin.ModelAdmin):
    list_display = ('id', 'status', 'payment_status', 'last_modified')
    search_fields = ('id', 'status', 'payment_status', 'last_modified')