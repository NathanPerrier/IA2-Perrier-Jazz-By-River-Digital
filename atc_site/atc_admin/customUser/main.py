from ..config import *


class CustomUserAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'is_superuser', 'is_staff', 'last_login')
    search_fields = ('email', 'is_superuser', 'is_staff', 'first_name', 'last_name')
    def save_model(self, request, obj, form, change):
        if 'password' in form.changed_data:
            obj.password = make_password(obj.password)
            
        try:
            stripe.Customer.modify(
                id=f'customuser-{str(obj.id)}',
                name=str(obj.first_name + ' ' + obj.last_name),
                email=obj.email,
            )
        except Exception as e:
            print(e)
            stripe.Customer.create(
                id=f'customuser-{str(obj.id)}',
                name=str(obj.first_name + ' ' + obj.last_name),
                email=obj.email,
            )
        super().save_model(request, obj, form, change)
        if not change:
            EmailAddress.objects.create(user=obj, email=obj.email, primary=True, verified=True)
    