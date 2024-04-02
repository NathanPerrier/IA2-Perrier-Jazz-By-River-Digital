from ..config import *

class ForgotPasswordAuthForm(forms.ModelForm):
    class Meta:
        model = ForgotPasswordAuth
        fields = '__all__'

    def clean_reset_code(self):
        reset_code = self.cleaned_data.get('reset_code')
        if reset_code and len(reset_code) != 6:
            raise ValidationError('Reset code must be 6 characters long')
        return reset_code

class ForgotPasswordAuthAdmin(admin.ModelAdmin):
    form = ForgotPasswordAuthForm
    list_display = ('user', 'reset_code', 'expiration_time')
    search_fields = ('user', 'reset_code', 'expiration_time')
    
    def save_model(self, request, obj, form, change):
        if 'reset_code' in form.changed_data:
            obj.reset_code = make_password(obj.reset_code)
        super().save_model(request, obj, form, change)