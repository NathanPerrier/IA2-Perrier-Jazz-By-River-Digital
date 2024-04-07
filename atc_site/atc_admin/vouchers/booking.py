from ..config import *

class BookingVoucherForm(forms.ModelForm):
    class Meta:
        model = Voucher
        fields = '__all__'
        
class BookingVouchersAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('voucher', 'user', 'booking')