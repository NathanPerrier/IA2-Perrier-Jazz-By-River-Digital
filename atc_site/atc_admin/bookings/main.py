from ..config import *

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = '__all__'
    
class BookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'event', 'tickets', 'payment', 'last_modified')
    search_fields = ('event', 'status')