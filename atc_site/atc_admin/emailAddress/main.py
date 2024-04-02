from ..config import * 

class EmailAddressForm(forms.ModelForm):
    class Meta:
        model = EmailAddress
        fields = '__all__'


class EmailAddressAdmin(admin.ModelAdmin):
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
