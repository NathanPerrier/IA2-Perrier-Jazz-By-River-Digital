from ..config import *

class BookingStatusForm(forms.ModelForm):
    class Meta:
        model = BookingStatus
        fields = '__all__'
        
    def clean_status(self):
        status = self.cleaned_data.get('status')
        if not status:
            raise ValidationError('Status is required')
        
        if status not in ['pending', 'confirmed', 'cancelled']:
            raise ValidationError('Invalid status, please sleect from pending, confirmed, cancelled')
        return status
    
    def clean_user(self):
        user = self.cleaned_data.get('user')
        if not user:
            raise ValidationError('User is required')
        if user not in CustomUser.objects.all():
            raise ValidationError('User does not exist')
        return user
    
    def clean_payment_status(self):
        payment_status = self.cleaned_data.get('payment_status')
        if not payment_status:
            raise ValidationError('Payment status is required')
        if payment_status not in PaymentStatus.objects.all():
            raise ValidationError('Invalid payment status')
        return payment_status
    
    def clean_stripe_invoice_id(self):
        stripe_invoice_id = self.cleaned_data.get('stripe_invoice_id')
        if stripe_invoice_id != self.instance.stripe_invoice_id:
            raise ValidationError("Stripe invoice ID cannot be changed")
        return stripe_invoice_id
        
class BookingStatusAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    form = BookingStatusForm
    list_display = ('id', 'status', 'payment_status', 'last_modified')
    search_fields = ('id', 'status', 'payment_status', 'last_modified')