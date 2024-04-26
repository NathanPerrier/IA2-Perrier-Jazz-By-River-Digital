from typing import Any
from ..config import *

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = '__all__'
        
    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        if amount < 1:
            raise ValidationError('Amount must be greater than 0')
        return amount
    
    def clean_user(self):
        user = self.cleaned_data.get('user')
        if user not in CustomUser.objects.all():
            raise ValidationError("CustomUser must be in the CustomUser group")
        return user

    def clean_currency(self):
        currency = self.cleaned_data.get('currency')
        if currency not in ['aud', 'usd', 'eur']:
            raise ValidationError("Currency must be aud, usd or eur")
        return currency
    
    def clean_method(self):
        method = self.cleaned_data.get('method')
        if method != self.instance.method: 
            raise ValidationError("Method cannot be changed")
        return method
    
    def clean_stripe_payment_id(self):
        stripe_payment_id = self.cleaned_data.get('stripe_payment_id')
        if stripe_payment_id != self.instance.stripe_payment_id:
            raise ValidationError("Stripe payment ID cannot be changed")
        return stripe_payment_id
    
    def clean_stripe_invoice_id(self):
        stripe_invoice_id = self.cleaned_data.get('stripe_invoice_id')
        if stripe_invoice_id != self.instance.stripe_invoice_id:
            raise ValidationError("Stripe invoice ID cannot be changed")
        return stripe_invoice_id
    
    def clean_status(self):
        status = self.cleaned_data.get('status')
        if status not in PaymentStatus.objects.all():
            raise ValidationError("Status must be one of the choices")
        return status

class PaymentAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    form = PaymentForm
    list_display = ('user', 'amount', 'currency', 'method', 'status', 'stripe_invoice_id', 'last_modified')
    search_fields = ('amount', 'method', 'status', 'last_modified')
    
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('<path:object_id>/delete/', self.admin_site.admin_view(self.delete_view), name='delete'),
        ]
        return custom_urls + urls
    
    def save_model(self, request, obj, form, change):
        obj.save()
        return super().save_model(request, obj, form, change)