import stripe
from decouple import config
from django.contrib.auth.decorators import login_required
from .main import *
from django.db.models import Count
from django.utils import timezone
import time, datetime
from .events.food_and_drinks.models import FoodAndDrinksItem, FoodAndDrinks, BookingFoodAndDrinks, EventFoodAndDrinks
from .events.models import Events, EventSchedule, EventScheduleItem
from .events.booking.models import Booking

stripe.api_key = config('STRIPE_API_KEY')

from django.contrib.auth import logout
from .email import send_contact_emails, send_newsletter_emails

@login_required
def admin_dashboard(request):
    if request.user.is_staff or request.user.is_superuser:
        return render(request, 'atc_site//admin//admin_dashboard.html', {'title': 'Overview', 'user': request.user, 'is_authenticated': request.user.is_authenticated, 
                                                                'top_selling_event': get_top_selling_event(),
                                                                'customers': stripe.Customer.list(), 
                                                                'income': get_income(),
                                                                'bookings': Booking.objects.all(), 
                                                                'events': Events.objects.all(),
                                                                "last_3_transactions": stripe.Invoice.list(limit=3)['data'],
                                                                'customers_percentage_increase': get_customers_percentage_increase(),
                                                                'customers_for_each_month_month': get_customers_for_each_month('month'), 'customers_for_each_month': get_customers_for_each_month(),
                                                                'income_for_each_month_month': get_income_for_each_month('month'), 'income_for_each_month': get_income_for_each_month(),
                                                                'bookings_for_each_month_month': get_booking_for_each_month('month'), 'bookings_for_each_month': get_booking_for_each_month(),})
    return render(request, 'atc_site//error.html', {'user': request.user, 'is_authenticated': request.user.is_authenticated, 'error': '400', 'title': 'Forbidden Access', 'desc': 'You do not have permission to access this page. If you believe this is an error, please contact the site administrator.'})


# other dashboard pages go here

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

#* VENDORS

@login_required
def vendor_items_dashboard(request):
    if request.user.is_staff or request.user.is_superuser:
        return render(request, 'atc_site//admin//vendor_items_dashboard.html', {'title': 'Vendor Dashboard', 'user': request.user, 'is_authenticated': request.user.is_authenticated, 'items': FoodAndDrinksItem.objects.all(), 'active_items': get_active_items()})

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
            return render(request, 'atc_site//admin//edit_item.html', {'title': 'Edit Item', 'user': request.user, 'is_authenticated': request.user.is_authenticated, 'item': item})
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
                total += amount['subtotal']
            payouts_for_each_month.append(total/100)
        except:
            payouts_for_each_month.append(0)
        
        
    
    print(payouts_for_each_month)
    return payouts_for_each_month[::-1]

def get_income():
    invoices = stripe.Invoice.list()['data']
    total = 0
    
    for transaction in invoices:
        total += transaction['subtotal']

    return total/100

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