import stripe
from decouple import config
from django.contrib.auth.decorators import login_required
from .main import *
from django.db.models import Count
from django.utils import timezone
import time, datetime

stripe.api_key = config('STRIPE_API_KEY')

from django.contrib.auth import logout
from .email import send_contact_emails, send_newsletter_emails

@login_required
def admin_dashboard(request):
    if request.user.is_staff or request.user.is_superuser:
        return render(request, 'atc_site//admin_dashboard.html', {'title': 'Overview', 'user': request.user, 'is_authenticated': request.user.is_authenticated, 
                                                                'top_selling_event': get_top_selling_event(),
                                                                'customers': stripe.Customer.list(), 
                                                                'income': (stripe.Balance.retrieve()['available'][0]['amount']+stripe.Balance.retrieve()['pending'][0]['amount']) / 100,
                                                                'bookings': Booking.objects.all(), 
                                                                'customers_percentage_increase': get_customers_percentage_increase(),
                                                                'customers_for_each_month_month': get_customers_for_each_month('month'), 'customers_for_each_month': get_customers_for_each_month(),
                                                                'income_for_each_month_month': get_income_for_each_month('month'), 'income_for_each_month': get_income_for_each_month(),
                                                                'bookings_for_each_month_month': get_booking_for_each_month('month'), 'bookings_for_each_month': get_booking_for_each_month(),})
    return render(request, 'atc_site//error.html', {'user': request.user, 'is_authenticated': request.user.is_authenticated, 'error': '400', 'title': 'Forbidden Access', 'desc': 'You do not have permission to access this page. If you believe this is an error, please contact the site administrator.'})


# other dashboard pages go here




# Methods


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
        month_data.append(stripe.BalanceTransaction.list(created={'lte': int(time.time()) - (86400*(i*30))})['data'])
    
    print(month_data)
    
    for transaction in month_data:
        total = 0
        try:
            for amount in transaction:
                total += amount['amount']
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