from ..config import *

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = '__all__'

class PaymentAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'method', 'status', 'last_modified')
    search_fields = ('amount', 'method', 'status', 'last_modified')