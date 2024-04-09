from ..config import * 

class EmailAddressForm(forms.ModelForm):
    class Meta:
        model = EmailAddress
        fields = '__all__'

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email:
            raise ValidationError('Email is required')
        elif email in EmailAddress.objects.values_list('email', flat=True):
            raise ValidationError('Email already exists')
        elif email not in CustomUser.objects.values_list('email', flat=True):
            raise ValidationError('Email does not exist')
        return email

class EmailAddressAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('user', 'email', 'primary', 'verified')
    search_fields = ('email', 'primary', 'verified')
    
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('<path:object_id>/delete/', self.admin_site.admin_view(self.delete_view), name='delete'),
        ]
        return custom_urls + urls

    def delete_view(self, request, object_id, extra_context=None):
        obj = self.get_object(request, object_id)
        if obj.primary:
            messages.error(request, 'Cannot delete primary email address')
            return redirect(request.META.get('HTTP_REFERER', '/'))
        else:
            return super().delete_view(request, object_id, extra_context)
