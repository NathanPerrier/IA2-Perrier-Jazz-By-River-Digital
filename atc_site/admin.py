from django.contrib import admin
from allauth.account.models import EmailAddress
from .models import CustomUser
from .backend.auth.register.models import RegisterAuth
from .backend.auth.forgot_password.models import ForgotPasswordAuth
from .backend.weather_app.locationImage.models import LocationImagesModel
from .backend.atc.events.models import Events, EventSchedule, EventScheduleItem
from .backend.atc.events.vouchers.models import Voucher, EventVoucher
from .backend.atc.events.food_and_drinks.models import FoodAndDrinks, EventFoodAndDrinks, FoodAndDrinksItem
from .backend.atc.events.booking.models import Booking, BookingStatus
from .backend.atc.events.booking.payment.models import Payment, PaymentStatus
from .backend.location.models import UserLocationModel
from .backend.weather_app.chatbot.models import Message, Route
from .backend.atc.chatbotATC.models import Message as ATCMessage
from .backend.atc.models import Newsletter

from django.contrib.auth.hashers import make_password


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
        

class CustomUserAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        if 'password' in form.changed_data:
            obj.password = make_password(obj.password)
        super().save_model(request, obj, form, change)
    
    def delete_model(self, request, obj):
        super().delete_model(request, obj)
        EmailAddress.objects.get(email=obj.email).delete()
        obj.delete()

# register custom tables

admin.site.register(CustomUser)
admin.site.register(RegisterAuth)
admin.site.register(ForgotPasswordAuth)
admin.site.register(LocationImagesModel)
admin.site.register(Events)
admin.site.register(EventSchedule)
admin.site.register(EventScheduleItem)
admin.site.register(Voucher)
admin.site.register(EventVoucher)
admin.site.register(FoodAndDrinks)
admin.site.register(EventFoodAndDrinks)
admin.site.register(FoodAndDrinksItem)
admin.site.register(Booking)
admin.site.register(BookingStatus)
admin.site.register(Payment)
admin.site.register(PaymentStatus)
admin.site.register(UserLocationModel)
admin.site.register(Message)
admin.site.register(Route)
admin.site.register(Newsletter)
admin.site.register(ATCMessage)

# update tables

admin.site.unregister(CustomUser)
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.unregister(EmailAddress)
admin.site.register(EmailAddress, EmailAddressAdmin)

admin.site.site_header = 'Ambrose Treacy College Admin Pannel'
admin.site.site_title = 'ATC Admin'