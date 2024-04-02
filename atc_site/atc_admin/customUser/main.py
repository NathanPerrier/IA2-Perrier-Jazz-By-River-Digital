from ..config import *


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'is_superuser', 'is_staff', 'last_login')
    search_fields = ('email', 'is_superuser', 'is_staff', 'first_name', 'last_name')
    def save_model(self, request, obj, form, change):
        if 'password' in form.changed_data:
            obj.password = make_password(obj.password)
        super().save_model(request, obj, form, change)
        if not change:
            EmailAddress.objects.create(user=obj, email=obj.email, primary=True, verified=True)
    