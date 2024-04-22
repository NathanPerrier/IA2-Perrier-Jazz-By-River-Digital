import stripe
from decouple import config
from django.contrib.auth.decorators import login_required
from .main import *
from django.db.models import Count
from django.utils import timezone
import time, datetime

stripe.api_key = config('STRIPE_API_KEY')

@login_required
def vendor_dashboard(request):
    if request.user.groups.filter(name='Vendor').exists():
        return render(request, 'atc_site//vendor//vendor_dashboard.html', {'title': 'Vendor Dashboard', 'user': request.user, 'is_authenticated': request.user.is_authenticated, 'vendor': request.user})
    return render(request, 'atc_site//error.html', {'user': request.user, 'is_authenticated': request.user.is_authenticated, 'error': '400', 'title': 'Forbidden Access', 'desc': 'You do not have permission to access this page. If you believe this is an error, please contact the site administrator.'})

@login_required
def vendor_items(request):
    if request.user.groups.filter(name='Vendor').exists():
        return render(request, 'atc_site//vendor//manage_items.html', {'title': 'Vendor Items', 'user': request.user, 'is_authenticated': request.user.is_authenticated, 'vendor': request.user})
    return render(request, 'atc_site//error.html', {'user': request.user, 'is_authenticated': request.user.is_authenticated, 'error': '400', 'title': 'Forbidden Access', 'desc': 'You do not have permission to access this page. If you believe this is an error, please contact the site administrator.'})

@login_required 
def vendor_orders(request):
    if request.user.groups.filter(name='Vendor').exists():
        return render(request, 'atc_site//vendor//manage_orders.html', {'title': 'Vendor Orders', 'user': request.user, 'is_authenticated': request.user.is_authenticated, 'vendor': request.user})
    return render(request, 'atc_site//error.html', {'user': request.user, 'is_authenticated': request.user.is_authenticated, 'error': '400', 'title': 'Forbidden Access', 'desc': 'You do not have permission to access this page. If you believe this is an error, please contact the site administrator.'})

@login_required
def vendor_order(request, order_id):
    if request.user.groups.filter(name='Vendor').exists():
        return render(request, 'atc_site//vendor//manage_order.html', {'title': 'Vendor Order', 'user': request.user, 'is_authenticated': request.user.is_authenticated, 'vendor': request.user})
    return render(request, 'atc_site//error.html', {'user': request.user, 'is_authenticated': request.user.is_authenticated, 'error': '400', 'title': 'Forbidden Access', 'desc': 'You do not have permission to access this page. If you believe this is an error, please contact the site administrator.'})

