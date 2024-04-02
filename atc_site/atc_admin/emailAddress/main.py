from ..config import * 

class EmailAddressAdmin(admin.ModelAdmin):
    list_display = ('user', 'email', 'primary', 'verified')
    search_fields = ('email', 'primary', 'verified')
    def delete_model(self, request, obj):
        user = CustomUser.objects.get(email=obj.email)
        super().delete_model(request, obj)
        user.delete()

    def delete_queryset(self, request, queryset):
        for obj in queryset:
            user = CustomUser.objects.get(email=obj.email)
            user.delete()
        super().delete_queryset(request, queryset)
        