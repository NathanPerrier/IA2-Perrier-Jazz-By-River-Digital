from ..config import *

class RegisterAuthForm(forms.ModelForm):
    class Meta:
        model = RegisterAuth
        fields = '__all__'

    def clean_reset_code(self):
        reset_code = self.cleaned_data.get('reset_code')
        if reset_code and len(reset_code) != 6:
            raise ValidationError('Reset code must be 6 characters long')
        return reset_code

class RegisterAuthAdmin(admin.ModelAdmin):
    form = RegisterAuthForm
    list_display = ('email', 'reset_code', 'expiration_time')
    search_fields = ('email', 'reset_code', 'expiration_time')
    
    def custom_field(self, obj):
        return obj.expiration_time - datetime.datetime.now()
    
    custom_field.short_description = 'Time to expire'

    def save_model(self, request, obj, form, change):
        if 'reset_code' in form.changed_data:
            obj.reset_code = make_password(obj.reset_code)
        super().save_model(request, obj, form, change)
         