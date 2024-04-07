from .atc_admin.__init__ import *
from .atc_admin.config import *

# register custom tables

admin.site.register(CustomUser) # -
admin.site.register(RegisterAuth, RegisterAuthAdmin) 
admin.site.register(ForgotPasswordAuth, ForgotPasswordAuthAdmin)
admin.site.register(LocationImagesModel, LocationImagesModelAdmin) 
admin.site.register(UserLocationModel, UserLocationModelAdmin) 
admin.site.register(Events, EventsAdmin) 
admin.site.register(EventSchedule, EventScheduleAdmin) 
admin.site.register(EventScheduleItem, EventScheduleItemAdmin) 
admin.site.register(Voucher, VoucherAdmin) 
admin.site.register(EventVoucher, EventVoucherAdmin)
admin.site.register(BookingVouchers, BookingVouchersAdmin)
admin.site.register(FoodAndDrinks, FoodAndDrinksAdmin)
admin.site.register(EventFoodAndDrinks, EventFoodAndDrinksAdmin)
admin.site.register(FoodAndDrinksItem, FoodAndDrinksItemAdmin)
admin.site.register(BookingFoodAndDrinks, BookingFoodAndDrinksAdmin)
admin.site.register(Booking, BookingAdmin)
admin.site.register(BookingStatus, BookingStatusAdmin)
admin.site.register(Tickets, TicketsAdmin)
admin.site.register(Payment, PaymentAdmin)
admin.site.register(PaymentStatus, PaymentStatusAdmin)
admin.site.register(Message, MessageAdmin)
admin.site.register(Route, RouteAdmin)
admin.site.register(Newsletter, NewsletterAdmin)
admin.site.register(ATCMessage, ATCMessageAdmin)

# update tables

admin.site.unregister(CustomUser)
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.unregister(EmailAddress)
admin.site.register(EmailAddress, EmailAddressAdmin)

admin.site.site_header = 'Ambrose Treacy College Admin Pannel'
admin.site.site_title = 'ATC Admin'