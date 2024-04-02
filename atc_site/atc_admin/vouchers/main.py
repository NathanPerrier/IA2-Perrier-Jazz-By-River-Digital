from ..config import *

class VoucherForm(forms.ModelForm):
    class Meta:
        model = Voucher
        fields = '__all__'
        
    def clean_code(self):
        cleaned_data = super().clean()
        code = cleaned_data.get('code')
        if 'code' in self.changed_data and code and len(code) != 6:
            raise ValidationError('Reset code must be 6 characters long')
        return cleaned_data


class VoucherAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    form = VoucherForm
    
    list_display = ('user', 'voucher', 'code', 'purchase_amount', 'amount_left', 'expiration_date')
    search_fields = ('voucher', 'purchase_amount', 'amount_left', 'expiration_date')
    
    def save_model(self, request, obj, form, change):
        if 'code' in form.changed_data:
            obj.code = make_password(obj.code)
        super().save_model(request, obj, form, change)