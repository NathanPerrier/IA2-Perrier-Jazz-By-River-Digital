from ..config import *

class PaymentStatusForm(forms.ModelForm):
    class Meta:
        model = PaymentStatus
        fields = '__all__'
    

class PaymentStatusAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('id', 'status', 'status_code', 'last_modified')
    search_fields = ('id', 'status', 'last_modified')