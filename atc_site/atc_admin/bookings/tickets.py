from ..config import *

class TicketsForm(forms.ModelForm):
    class Meta:
        model = Tickets
        fields = '__all__'
        
    def clean_event(self):
        event = self.cleaned_data.get('event')
        if not event:
            raise ValidationError('Event is required')
        if event not in Events.objects.all():
            raise ValidationError('Event does not exist')
        return event
    
    def clean_user(self):
        user = self.cleaned_data.get('user')
        if not user:
            raise ValidationError('User is required')
        if user not in CustomUser.objects.all():
            raise ValidationError('User does not exist')
        return user

    def clean_stripe_invoice_id(self):
        stripe_invoice_id = self.cleaned_data.get('stripe_invoice_id')
        if stripe_invoice_id != self.instance.stripe_invoice_id:
            raise ValidationError("Stripe invoice ID cannot be changed")
        return stripe_invoice_id
    
class TicketsAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    form = TicketsForm
    list_display = ('user', 'event', 'sent')

    
    