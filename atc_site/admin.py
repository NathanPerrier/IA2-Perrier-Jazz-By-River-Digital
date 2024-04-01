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
admin.site.site_header = 'Ambrose Treacy College Admin Pannel'
admin.site.site_title = 'ATC Admin'