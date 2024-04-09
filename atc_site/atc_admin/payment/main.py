from ..config import *

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = '__all__'

class PaymentAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('user', 'amount', 'currency', 'method', 'status', 'stripe_invoice_id', 'last_modified')
    search_fields = ('amount', 'method', 'status', 'last_modified')
    
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('<path:object_id>/delete/', self.admin_site.admin_view(self.delete_view), name='delete'),
        ]
        return custom_urls + urls