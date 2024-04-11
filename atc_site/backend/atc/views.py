import os
from django.http import StreamingHttpResponse, JsonResponse
from django.conf import settings
from .models import Newsletter
import stripe
from decouple import config
from django.contrib.auth.decorators import login_required
from .main import *
from django.utils import timezone
import time, datetime

stripe.api_key = config('STRIPE_API_KEY')

from django.contrib.auth import logout
from .email import send_contact_emails, send_newsletter_emails

def logout_view(request):
    logout(request)
    return index(request)

def register_view(request):
    return register_page(request)
    
def forgot_password_view(request):
    return forgot_password_page(request)

@login_required
def billing_portal_view(request):
    configuration = stripe.billing_portal.Configuration.create(
        features={
            'customer_update': {
            'allowed_updates': ['tax_id', 'address', 'phone'],
            'enabled': True,
            },
            'invoice_history': {
            'enabled': True,
            },
            'payment_method_update': {
            'enabled': True,
            },
        },
        business_profile={
            'privacy_policy_url': 'http://localhost:8000/terms%20and%20policies/privacy%20policy',
            'terms_of_service_url': 'http://localhost:8000/terms%20and%20policies/terms%20and%20conditions',
        },
    )
    billing_portal = stripe.billing_portal.Session.create(
        customer=f'customuser-{str(request.user.id)}',
        return_url="http://localhost:8000/",
        configuration=configuration.id,
    )
   
    return redirect(billing_portal.url)

@login_required
def stripe_dashboard(request):
    account = stripe.Account.create_login_link(f'customuser-{str(request.user.id)}')
    return redirect(account.url, code=303)

@login_required
def admin_dashboard(request):
    if request.user.is_staff or request.user.is_superuser:
        return render(request, 'atc_site//admin_dashboard.html', {'user': request.user, 'is_authenticated': request.user.is_authenticated, 
                                                                'customers': stripe.Customer.list(), 
                                                                'income': (stripe.Balance.retrieve()['available'][0]['amount']+stripe.Balance.retrieve()['pending'][0]['amount']) / 100,
                                                                'bookings': Booking.objects.all(), 
                                                                'customers_percentage_increase': get_customers_percentage_increase(),
                                                                'customers_for_each_month_month': get_customers_for_each_month('month'), 'customers_for_each_month': get_customers_for_each_month(),
                                                                'income_for_each_month_month': get_income_for_each_month('month'), 'income_for_each_month': get_income_for_each_month(),
                                                                'bookings_for_each_month_month': get_booking_for_each_month('month'), 'bookings_for_each_month': get_booking_for_each_month(),})
    return render(request, 'atc_site//error.html', {'user': request.user, 'is_authenticated': request.user.is_authenticated, 'error': '400', 'title': 'Forbidden Access', 'desc': 'You do not have permission to access this page. If you believe this is an error, please contact the site administrator.'})

def stream_video_atc_site(request, video_path):
    video_path = os.path.join(settings.BASE_DIR, 'atc_site\\frontend\\static\\atc_site\\videos', video_path)
    def play_video(video_path):
        with open(video_path, 'rb') as video:
            for chunk in iter(lambda: video.read(4096), b""):
                yield chunk

    response = StreamingHttpResponse(play_video(video_path))
    response['Content-Type'] = 'video/mp4'
    return response


def contact_ajax(request):
    print("contact_ajax")
    if request.method == 'POST':
        print(request.POST['name'])
        send_contact_emails(request.POST['email'], settings.EMAIL_HOST_USER, request.POST['name'], request.POST['subject'], request.POST['message'])
        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False})
    
def newsletter_ajax(request):
    if request.method == 'POST':
        email = request.POST['email']
        if Newsletter.objects.filter(email=email).exists():
            return JsonResponse({'success': False})
        else:
            send_newsletter_emails(email, settings.EMAIL_HOST_USER)
            Newsletter.objects.create(email=email)
            return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False})
    
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