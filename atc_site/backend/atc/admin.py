import stripe
from decouple import config
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from .main import *
from django.db.models import Count
from django.utils import timezone
import time, datetime
from .events.food_and_drinks.models import FoodAndDrinksItem, FoodAndDrinks, BookingFoodAndDrinks, EventFoodAndDrinks
from .events.vouchers.models import Voucher, BookingVouchers
from .events.models import Events, EventSchedule, EventScheduleItem
from .events.booking.models import Booking, BookingStatus
from .events.booking.tickets.models import Tickets
from .events.booking.payment.models import Payment, PaymentStatus
from ...models import CustomUser
from .email import send_custom_emails
from .events.booking.models import Booking

stripe.api_key = config('STRIPE_API_KEY')

@login_required
def admin_dashboard(request):
    if request.user.is_staff or request.user.is_superuser:
        return render(request, 'atc_site//admin//admin_dashboard.html', {'title': 'Overview', 'user': request.user, 'is_authenticated': request.user.is_authenticated, 
                                                                'top_selling_event': get_top_selling_event(),
                                                                'customers': stripe.Customer.list(), 
                                                                'income': (stripe.Balance.retrieve()['available'][0]['amount']+stripe.Balance.retrieve()['pending'][0]['amount'])/100,
                                                                'bookings': Booking.objects.all(), 
                                                                'events': Events.objects.all(),
                                                                "last_3_transactions": stripe.Invoice.list(limit=3)['data'],
                                                                'customers_percentage_increase': get_customers_percentage_increase(),
                                                                'customers_for_each_month_month': get_customers_for_each_month('month'), 'customers_for_each_month': get_customers_for_each_month(),
                                                                'income_for_each_month_month': get_income_for_each_month('month'), 'income_for_each_month': get_income_for_each_month(),
                                                                'bookings_for_each_month_month': get_booking_for_each_month('month'), 'bookings_for_each_month': get_booking_for_each_month(),})
    return render(request, 'atc_site//error.html', {'user': request.user, 'is_authenticated': request.user.is_authenticated, 'error': '400', 'title': 'Forbidden Access', 'desc': 'You do not have permission to access this page. If you believe this is an error, please contact the site administrator.'})


# other dashboard pages go here

#* USERS

@login_required
def users_dashboard(request):
    if request.user.is_staff or request.user.is_superuser:
        return render(request, 'atc_site//admin//users_dashboard.html', {'title': 'Users Dashboard', 'user': request.user, 'is_authenticated': request.user.is_authenticated, 'users': CustomUser.objects.all()})
    return render(request, 'atc_site//error.html', {'user': request.user, 'is_authenticated': request.user.is_authenticated, 'error': '400', 'title': 'Forbidden Access', 'desc': 'You do not have permission to access this page. If you believe this is an error, please contact the site administrator.'})

@login_required
def delete_user(request, user_id):
    if request.user.is_staff or request.user.is_superuser:
        try:
            BookingFoodAndDrinks.objects.filter(user=CustomUser.objects.get(id=user_id)).delete()  
            FoodAndDrinks.objects.filter(user=CustomUser.objects.get(id=user_id)).delete()
            BookingVouchers.objects.filter(user=CustomUser.objects.get(id=user_id)).delete()
            Voucher.objects.filter(user=CustomUser.objects.get(id=user_id)).delete()
            Booking.objects.filter(user=CustomUser.objects.get(id=user_id)).delete()
            CustomUser.objects.get(id=user_id).delete()
            return redirect('/admin/dashboard/users/')
        except Exception as e: return render(request, 'atc_site//error.html', {'user': request.user, 'is_authenticated': request.user.is_authenticated, 'error': '403', 'title': 'Bad Request', 'desc': f'{e}. If you believe this is an error, please contact the site administrator.'})
    return render(request, 'atc_site//error.html', {'user': request.user, 'is_authenticated': request.user.is_authenticated, 'error': '400', 'title': 'Forbidden Access', 'desc': 'You do not have permission to access this page. If you believe this is an error, please contact the site administrator.'})

#* BOOKINGS

@login_required
def bookings_dashboard(request):
    if request.user.is_staff or request.user.is_superuser:
        return render(request, 'atc_site//admin//bookings_dashboard.html', {'title': 'Bookings Dashboard', 'user': request.user, 'is_authenticated': request.user.is_authenticated, 'bookings': get_invoices_for_bookings(Booking.objects.all())})
    return render(request, 'atc_site//error.html', {'user': request.user, 'is_authenticated': request.user.is_authenticated, 'error': '400', 'title': 'Forbidden Access', 'desc': 'You do not have permission to access this page. If you believe this is an error, please contact the site administrator.'})


@login_required
def delete_booking(request, booking_id):
    if request.user.is_staff or request.user.is_superuser:
        try:
            obj = Booking.objects.get(id=booking_id)
            payment_intent = stripe.PaymentIntent.retrieve(obj.payment.stripe_payment_id)

            try:                     
                refund = stripe.Refund.create(
                    payment_intent=payment_intent,
                )
            except: print('refund error')
           
            food_and_drink_items = BookingFoodAndDrinks.objects.filter(booking=obj)
            for item in food_and_drink_items:
                item.food_and_drinks.item.food_and_drinks_item.stock += item.food_and_drinks.quantity
                item.food_and_drinks.item.food_and_drinks_item.quantity_sold -= item.food_and_drinks.quantity
                item.food_and_drinks.item.food_and_drinks_item.save()
                item.food_and_drinks.delete()
            
            BookingFoodAndDrinks.objects.filter(booking=obj).delete() #? obj.id?
            booking_vouchers = BookingVouchers.objects.filter(booking=obj)
            
            for voucher in booking_vouchers:
                stripe.Coupon.delete(voucher.voucher.stripe_coupon_id)
                voucher.voucher.delete()
                voucher.delete()
            
            Tickets.objects.get(stripe_invoice_id=obj.stripe_invoice_id).delete()
            Payment.objects.get(stripe_invoice_id=obj.stripe_invoice_id).delete()
            BookingStatus.objects.get(stripe_invoice_id=obj.stripe_invoice_id).delete()
            
        except Exception as e: return render(request, 'atc_site//error.html', {'user': request.user, 'is_authenticated': request.user.is_authenticated, 'error': '403', 'title': 'Bad Request', 'desc': f'{e}. If you believe this is an error, please contact the site administrator.'})
            
        event = obj.event
        event.available_tickets += 1
        event.sold -= 1
        event.save()
        
        obj.delete()
        
        return redirect('/admin/dashboard/bookings/')
    return render(request, 'atc_site//error.html', {'user': request.user, 'is_authenticated': request.user.is_authenticated, 'error': '400', 'title': 'Forbidden Access', 'desc': 'You do not have permission to access this page. If you believe this is an error, please contact the site administrator.'})

#* EVENTS

@login_required
def events_dashboard(request):
    if request.user.is_staff or request.user.is_superuser:
        return render(request, 'atc_site//admin//events_dashboard.html', {'title': 'Events Dashboard', 'user': request.user, 'is_authenticated': request.user.is_authenticated, 'events': Events.objects.all(), 'now': timezone.now()})
    return render(request, 'atc_site//error.html', {'user': request.user, 'is_authenticated': request.user.is_authenticated, 'error': '400', 'title': 'Forbidden Access', 'desc': 'You do not have permission to access this page. If you believe this is an error, please contact the site administrator.'})

@login_required
def delete_event(request, event_id):
    if request.user.is_staff or request.user.is_superuser:
        try:
            event = Events.objects.get(id=event_id)
            EventFoodAndDrinks.objects.filter(event=event).delete()
            FoodAndDrinksItem.objects.filter(event=event).delete()
            EventSchedule.objects.filter(event=event).delete()
            Booking.objects.filter(event=event).delete()
            
            event.delete()
            return redirect('/admin/dashboard/events/')
        except Exception as e:
            print(e)
            return render(request, 'atc_site//error.html', {'user': request.user, 'is_authenticated': request.user.is_authenticated, 'error': '400', 'title': 'Forbidden Access', 'desc': 'You do not have permission to access this page. If you believe this is an error, please contact the site administrator.'})
    return render(request, 'atc_site//error.html', {'user': request.user, 'is_authenticated': request.user.is_authenticated, 'error': '400', 'title': 'Forbidden Access', 'desc': 'You do not have permission to access this page. If you believe this is an error, please contact the site administrator.'})

#* VOUCHERS

@login_required
def vouchers_dashboard(request):
    if request.user.is_staff or request.user.is_superuser:
        return render(request, 'atc_site//admin//vouchers_dashboard.html', {'title': 'Vouchers Dashboard', 'user': request.user, 'is_authenticated': request.user.is_authenticated, 'vouchers': Voucher.objects.all()})
    return render(request, 'atc_site//error.html', {'user': request.user, 'is_authenticated': request.user.is_authenticated, 'error': '400', 'title': 'Forbidden Access', 'desc': 'You do not have permission to access this page. If you believe this is an error, please contact the site administrator.'})

@login_required
def delete_voucher(request, voucher_id):
    if request.user.is_staff or request.user.is_superuser:
        try:
            voucher = Voucher.objects.get(id=voucher_id)
            BookingVouchers.objects.filter(voucher=voucher).delete()
            EventVoucher.objects.filter(voucher=voucher).delete()
            stripe.Coupon.retrieve(voucher.stripe_coupon_id).delete()
            voucher.delete()
            return redirect('/admin/dashboard/vouchers/')
        except Exception as e: return render(request, 'atc_site//error.html', {'user': request.user, 'is_authenticated': request.user.is_authenticated, 'error': '403', 'title': 'Bad Request', 'desc': f'{e}. If you believe this is an error, please contact the site administrator.'})
    return render(request, 'atc_site//error.html', {'user': request.user, 'is_authenticated': request.user.is_authenticated, 'error': '400', 'title': 'Forbidden Access', 'desc': 'You do not have permission to access this page. If you believe this is an error, please contact the site administrator.'})

@login_required
def send_voucher(request, voucher_id):
    if request.user.is_staff or request.user.is_superuser:
        voucher = Voucher.objects.get(id=voucher_id)
        code = stripe.PromotionCode.retrieve(voucher.stripe_code_id)
        try:
            send_custom_emails(request.user.email, request.user.first_name, 'Voucher Purchased', f'Thank you for purchasing a voucher for {voucher.event.name}, this voucher can be used online or in-person. \nYour code is: \n \n {code.code}')
            voucher.sent = True
        except Exception as e: 
            print(e)
            voucher.sent = False
        voucher.save()
        return redirect('/admin/dashboard/vouchers/')
    return render(request, 'atc_site//error.html', {'user': request.user, 'is_authenticated': request.user.is_authenticated, 'error': '400', 'title': 'Forbidden Access', 'desc': 'You do not have permission to access this page. If you believe this is an error, please contact the site administrator.'})

#* VENDORS

@login_required
def vendors_dashboard(request):
    if request.user.is_staff or request.user.is_superuser:
        return render(request, 'atc_site//admin//vendors_dashboard.html', {'title': 'Vendor Dashboard', 'user': request.user, 'is_authenticated': request.user.is_authenticated, 'vendors': get_vendors()})
    return render(request, 'atc_site//error.html', {'user': request.user, 'is_authenticated': request.user.is_authenticated, 'error': '400', 'title': 'Forbidden Access', 'desc': 'You do not have permission to access this page. If you believe this is an error, please contact the site administrator.'})


@login_required
def delete_vendor(request, vendor_id):
    if request.user.is_staff or request.user.is_superuser:
        try:
            vendor = CustomUser.objects.get(id=vendor_id)
            FoodAndDrinksItem.objects.filter(vendor=vendor).delete()
            EventFoodAndDrinks.objects.filter(food_and_drinks_item__vendor=vendor).delete()
            vendor_group = Group.objects.get(name='Vendor')  
            vendor.groups.remove(vendor_group)  
            vendor.save()
            return redirect('/admin/dashboard/vendors/')
        except Exception as e: return render(request, 'atc_site//error.html', {'user': request.user, 'is_authenticated': request.user.is_authenticated, 'error': '403', 'title': 'Bad Request', 'desc': f'{e}. If you believe this is an error, please contact the site administrator.'})
    return render(request, 'atc_site//error.html', {'user': request.user, 'is_authenticated': request.user.is_authenticated, 'error': '400', 'title': 'Forbidden Access', 'desc': 'You do not have permission to access this page. If you believe this is an error, please contact the site administrator.'})

@login_required
def vendor_items_dashboard(request):
    if request.user.is_staff or request.user.is_superuser:
        return render(request, 'atc_site//admin//vendor_items_dashboard.html', {'title': 'Vendor Dashboard', 'user': request.user, 'is_authenticated': request.user.is_authenticated, 'items': FoodAndDrinksItem.objects.all(), 'active_items': get_active_items()})
    return render(request, 'atc_site//error.html', {'user': request.user, 'is_authenticated': request.user.is_authenticated, 'error': '400', 'title': 'Forbidden Access', 'desc': 'You do not have permission to access this page. If you believe this is an error, please contact the site administrator.'})

@login_required
def activate_item(request, item_id):
    if request.user.is_staff or request.user.is_superuser:
        try:
            item = FoodAndDrinksItem.objects.get(id=item_id)
            EventFoodAndDrinks.objects.create(event=item.event, food_and_drinks_item=item)
            return redirect('vendor_items_dashboard')
        except: return render(request, 'atc_site//error.html', {'user': request.user, 'is_authenticated': request.user.is_authenticated, 'error': '400', 'title': 'Forbidden Access', 'desc': 'You do not have permission to access this page. If you believe this is an error, please contact the site administrator.'})
    return render(request, 'atc_site//error.html', {'user': request.user, 'is_authenticated': request.user.is_authenticated, 'error': '400', 'title': 'Forbidden Access', 'desc': 'You do not have permission to access this page. If you believe this is an error, please contact the site administrator.'})

@login_required
def deactivate_item(request, item_id):
    if request.user.is_staff or request.user.is_superuser:
        try:
            item = FoodAndDrinksItem.objects.get(id=item_id)
            EventFoodAndDrinks.objects.get(event=item.event, food_and_drinks_item=item).delete()
            return redirect('vendor_items_dashboard')
        except: return render(request, 'atc_site//error.html', {'user': request.user, 'is_authenticated': request.user.is_authenticated, 'error': '400', 'title': 'Forbidden Access', 'desc': 'You do not have permission to access this page. If you believe this is an error, please contact the site administrator.'})
    return render(request, 'atc_site//error.html', {'user': request.user, 'is_authenticated': request.user.is_authenticated, 'error': '400', 'title': 'Forbidden Access', 'desc': 'You do not have permission to access this page. If you believe this is an error, please contact the site administrator.'})

@login_required
def edit_item(request, item_id):
    if request.user.is_staff or request.user.is_superuser:
        try:
            item = FoodAndDrinksItem.objects.get(id=item_id)
            if request.method == 'POST':           
                try: 
                    item.name = request.POST['name'].capitalize()
                    item.price = float(request.POST['price'])
                    item.stock = int(request.POST['stock'])
                    item.description = request.POST['description']
                    item.image = request.FILES['image'] if request.FILES else item.image
                    item.event=Events.objects.get(id=request.POST['event'])
                    
                    try:
                        product = stripe.Product.create(
                            id=f'food-and-drinks-{str(item.id)}',
                            name=item.name.capitalize(),
                            active=True,
                            description=item.description,
                        )
                        
                        price = stripe.Price.create(
                            product=product.id,
                            unit_amount=int(item.price*100),  
                            currency="aud",
                        )
                        
                        stripe.Product.modify(
                            id=product.id,
                            default_price=price.id,
                        )
                        
                        for voucher in Voucher.objects.filter(event=item.event):
                            stripe.Coupon.modify(
                                id=f'voucher-{str(voucher.id)}',
                                applies_to={'products':[f'food-and-drinks-{item.id}' for item in FoodAndDrinksItem.objects.filter(event=item.event)]},
                            )
                            
                    except Exception as e:
                        print(e)
                        product = stripe.Product.modify(
                            id=f'food-and-drinks-{str(item.id)}',
                            name=item.name.capitalize(),
                            active=True,
                            description=item.description,
                        )
                        price = stripe.Price.create(
                            product=product.id,
                            unit_amount=int(item.price*100),  
                            currency="aud",
                        )
                        
                        stripe.Product.modify(
                            id=product.id,
                            default_price=price.id,
                        )
                    
                    item.stripe_price_id = price.id
                    item.stripe_product_id = product.id
                    item.save()
                    try: EventFoodAndDrinks.objects.get(food_and_drinks_item=item).delete()
                    except: pass
                except Exception as e:
                    print(e)
                    return JsonResponse({'success': False, 'error': str(e)})
                return redirect('/vendor/dashboard/items/')
            return render(request, 'atc_site//admin//edit_item.html', {'title': 'Edit Item', 'user': request.user, 'is_authenticated': request.user.is_authenticated, 'item': item, 'active_events': Events.objects.filter(date__gte=timezone.now()).all()})
        except: return render(request, 'atc_site//error.html', {'user': request.user, 'is_authenticated': request.user.is_authenticated, 'error': '400', 'title': 'Forbidden Access', 'desc': 'You do not have permission to access this page. If you believe this is an error, please contact the site administrator.'})
    return render(request, 'atc_site//error.html', {'user': request.user, 'is_authenticated': request.user.is_authenticated, 'error': '400', 'title': 'Forbidden Access', 'desc': 'You do not have permission to access this page. If you believe this is an error, please contact the site administrator.'})

@login_required
def delete_item(request, item_id):
    if request.user.is_staff or request.user.is_superuser:
        try:
            item = FoodAndDrinksItem.objects.get(id=item_id)
            item.delete()
            return redirect('vendor_items_dashboard')
        except: return render(request, 'atc_site//error.html', {'user': request.user, 'is_authenticated': request.user.is_authenticated, 'error': '400', 'title': 'Forbidden Access', 'desc': 'You do not have permission to access this page. If you believe this is an error, please contact the site administrator.'})
    return render(request, 'atc_site//error.html', {'user': request.user, 'is_authenticated': request.user.is_authenticated, 'error': '400', 'title': 'Forbidden Access', 'desc': 'You do not have permission to access this page. If you believe this is an error, please contact the site administrator.'})


#* STRIPE

@login_required
def stripe_invoice_dashboard(request):
    if request.user.is_staff or request.user.is_superuser:
        return render(request, 'atc_site//admin//stripe_invoice_dashboard.html', {'title': 'Stripe Invoice Dashboard', 'user': request.user, 'is_authenticated': request.user.is_authenticated, 'invoices': get_stripe_invoices()})
    return render(request, 'atc_site//error.html', {'user': request.user, 'is_authenticated': request.user.is_authenticated, 'error': '400', 'title': 'Forbidden Access', 'desc': 'You do not have permission to access this page. If you believe this is an error, please contact the site administrator.'})



#* Other

def get_customers_percentage_increase():
    if len(stripe.Customer.list(created={'gte': int(time.time()) - 86400})) > 0:
        percentage = (len(stripe.Customer.list()) - len(stripe.Customer.list(created={'gte': int(time.time()) - 86400}))/len(stripe.Customer.list(created={'gte': int(time.time()) - 86400})))*100
        if percentage > 100 or percentage < -100: percentage = 100 if percentage > 0 else -100
        return f'+{percentage}%' if percentage > 0 else f'-{percentage}%'
    return '+100%'

def get_customers_for_each_month(option=False):
    """ get 6 month data of number of stripe customers """
    months = []
    for i in range(6):
        i=abs(i-6)
        month = datetime.datetime.now() - datetime.timedelta(days=30*i)
        months.append(month.strftime('%B'))
    
    if option:
        return months
    
    print(months)
    
    customers_for_each_month = []
    for i, month in enumerate(months):
        customers_for_each_month.append(len(stripe.Customer.list(created={'lte': int(time.time()) - (86400*(i*30))})))
        
    print(customers_for_each_month)
    return customers_for_each_month[::-1]

def get_income_for_each_month(option=False):
    months = []
    for i in range(6):
        i=abs(i-6)
        month = datetime.datetime.now() - datetime.timedelta(days=30*i)
        months.append(month.strftime('%B'))
    
    if option:
        return months
    
    payouts_for_each_month = []
    month_data = []
    for i, month in enumerate(months):
        month_data.append(stripe.Invoice.list(created={'lte': int(time.time()) - (86400*(i*30))})['data'])
    
    print(month_data)
    
    for transaction in month_data:
        total = 0
        try:
            for amount in transaction:
                if amount.id in [booking.stripe_invoice_id for booking in Booking.objects.all()]:
                    total += amount['subtotal']
            payouts_for_each_month.append(total/100)
        except:
            payouts_for_each_month.append(0)
        
        
    
    print(payouts_for_each_month)
    return payouts_for_each_month[::-1]


def get_booking_for_each_month(option=False):
    months = []
    for i in range(6):
        i=abs(i-6)
        month = datetime.datetime.now() - datetime.timedelta(days=30*i)
        months.append(month.strftime('%B'))
    
    if option:
        return months
    
    bookings_for_each_month = []
    for i, month in enumerate(months):
        bookings_for_each_month.append(len(Booking.objects.filter(creation_time__lte=timezone.now() - timezone.timedelta(days=30*i))))
        
    print(bookings_for_each_month)
    return bookings_for_each_month[::-1]

def get_top_selling_event():
    return Events.objects.filter(
        date__gt=timezone.now(),
        sale_release_date__lt=timezone.now(),
        sale_end_date__gt=timezone.now()
    ).annotate(tickets_sold=Count('tickets')).order_by('-tickets_sold').first()
    
def get_active_items():
    items = EventFoodAndDrinks.objects.all()
    active_items = []
    
    for item in items:
        active_items.append(item.food_and_drinks_item)
        
    return active_items

def get_invoices_for_bookings(bookings):
    invoices=[]
    for booking in bookings:
        invoices.append([booking, stripe.Invoice.retrieve(booking.stripe_invoice_id)])
    return invoices

def get_vendors():
    vendors = []
    for vendor in CustomUser.objects.filter(groups=Group.objects.get(name='Vendor')):
        revenue = 0
        for order in FoodAndDrinks.objects.filter(item__food_and_drinks_item__vendor=vendor):
            revenue += order.item.food_and_drinks_item.price * order.quantity
        vendors.append([vendor, FoodAndDrinksItem.objects.filter(vendor=vendor).all(), revenue])
        
    return vendors

def get_stripe_invoices():
    invoices = []
    for invoice in stripe.Invoice.list():
        for booking in Booking.objects.all():
            if invoice.id == booking.stripe_invoice_id:
                invoices.append([invoice, booking])
    return invoices

