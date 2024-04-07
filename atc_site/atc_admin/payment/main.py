from ..config import *

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = '__all__'

class PaymentAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('user', 'amount', 'currency', 'method', 'status', 'stripe_invoice_id', 'last_modified')
    search_fields = ('amount', 'method', 'status', 'last_modified')