from .atc_admin.__init__ import *
from .atc_admin.config import *

# register custom tables

admin.site.register(CustomUser) # -
admin.site.register(RegisterAuth, RegisterAuthAdmin) 
admin.site.register(ForgotPasswordAuth, ForgotPasswordAuthAdmin)
admin.site.register(LocationImagesModel)
admin.site.register(UserLocationModel)
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