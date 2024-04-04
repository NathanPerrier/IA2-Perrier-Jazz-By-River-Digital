from ..config import *

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = '__all__'
    
class BookingAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('user', 'event', 'ticket', 'payment', 'last_modified')
    search_fields = ('event', 'status')