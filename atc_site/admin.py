# from django.contrib import admin
# from allauth.account.models import EmailAddress
# from .models import CustomUser
# class EmailAddressAdmin(admin.ModelAdmin):
#     def delete_model(self, request, obj):
#         user = obj.user
#         print(user)
#         CustomUser().delete_by_id(user.id)
#         super().delete_model(request, obj)
#         user.delete()

# admin.site.unregister(EmailAddress)
# admin.site.register(EmailAddress, EmailAddressAdmin)

from django.contrib import admin
from allauth.account.models import EmailAddress
from .models import CustomUser
from .models import CustomUser

class EmailAddressAdmin(admin.ModelAdmin):
    def delete_model(self, request, obj):
        user = CustomUser.objects.get(email=obj.email)
        super().delete_model(request, obj)
        user.delete()

    def delete_queryset(self, request, queryset):
        for obj in queryset:
            user = CustomUser.objects.get(email=obj.email)
            user.delete()
        super().delete_queryset(request, queryset)

admin.site.unregister(EmailAddress)
admin.site.register(EmailAddress, EmailAddressAdmin)

# register custom tables

admin.site.register(CustomUser)