import stripe
from decouple import config
from django.contrib.auth.decorators import login_required
from .main import *
from django.db.models import Count
from django.utils import timezone
import time, datetime
from .events.food_and_drinks.models import FoodAndDrinksItem, FoodAndDrinks, BookingFoodAndDrinks, EventFoodAndDrinks

stripe.api_key = config('STRIPE_API_KEY')

@login_required
def vendor_dashboard(request):
    if request.user.groups.filter(name='Vendor').exists():
        return render(request, 'atc_site//vendor//vendor_dashboard.html', {'title': 'Vendor Dashboard', 'user': request.user, 'is_authenticated': request.user.is_authenticated, 'vendor': request.user})
    return render(request, 'atc_site//error.html', {'user': request.user, 'is_authenticated': request.user.is_authenticated, 'error': '400', 'title': 'Forbidden Access', 'desc': 'You do not have permission to access this page. If you believe this is an error, please contact the site administrator.'})

@login_required
def vendor_items(request):
    if request.user.groups.filter(name='Vendor').exists():
        return render(request, 'atc_site//vendor//manage_items.html', {'title': 'Manage Items', 'user': request.user, 'is_authenticated': request.user.is_authenticated, 'vendor': request.user, 'items': FoodAndDrinksItem.objects.filter(vendor=request.user).all(), 'active_items': EventFoodAndDrinks.objects.filter(food_and_drinks_item__vendor=request.user).values('food_and_drinks_item')})
    return render(request, 'atc_site//error.html', {'user': request.user, 'is_authenticated': request.user.is_authenticated, 'error': '400', 'title': 'Forbidden Access', 'desc': 'You do not have permission to access this page. If you believe this is an error, please contact the site administrator.'})

@login_required
def vendor_item(request, item_id):
    if request.user.groups.filter(name='Vendor').exists():
        try:
            item = FoodAndDrinksItem.objects.get(id=item_id)
            if request.user == item.vendor: return render(request, 'atc_site//vendor//view_item.html', {'title': 'Edit Item', 'user': request.user, 'is_authenticated': request.user.is_authenticated, 'vendor': request.user, 'item': item})
        except: return render(request, 'atc_site//error.html', {'user': request.user, 'is_authenticated': request.user.is_authenticated, 'error': '403', 'title': 'Bad Request', 'desc': 'An error occured loading this page, if you believe this is an error, please contact the site administrator.'})
    return render(request, 'atc_site//error.html', {'user': request.user, 'is_authenticated': request.user.is_authenticated, 'error': '400', 'title': 'Forbidden Access', 'desc': 'You do not have permission to access this page. If you believe this is an error, please contact the site administrator.'})



@login_required  
def vendor_orders(request):
    if request.user.groups.filter(name='Vendor').exists():
        try:
            #get items from FoodandDrinks where item.item.vendor is request.user
            orders = get_vendor_orders(request.user)
            return render(request, 'atc_site//vendor//manage_orders.html', {'title': 'Manage Orders', 'user': request.user, 'is_authenticated': request.user.is_authenticated, 'vendor': request.user, 'orders': orders})
        except Exception as e: 
            print(e)
            return render(request, 'atc_site//error.html', {'user': request.user, 'is_authenticated': request.user.is_authenticated, 'error': '403', 'title': 'Bad Request', 'desc': 'An error occured loading this page, if you believe this is an error, please contact the site administrator.'})
    return render(request, 'atc_site//error.html', {'user': request.user, 'is_authenticated': request.user.is_authenticated, 'error': '400', 'title': 'Forbidden Access', 'desc': 'You do not have permission to access this page. If you believe this is an error, please contact the site administrator.'})

@login_required
def vendor_order(request, order_id):
    if request.user.groups.filter(name='Vendor').exists():
        try:
            order = FoodAndDrinks.objects.get(id=order_id)
            booking_order = BookingFoodAndDrinks.objects.get(food_and_drinks=order)
            payment_intent = stripe.PaymentIntent.retrieve(booking_order.booking.payment.stripe_payment_id)
            if order.vendor == request.user: return render(request, 'atc_site//vendor//manage_order.html', {'title': 'Vendor Order', 'user': request.user, 'is_authenticated': request.user.is_authenticated, 'vendor': request.user, 'order': order, 'booking_order': booking_order, 'payment_intent': payment_intent})
        except: return render(request, 'atc_site//error.html', {'user': request.user, 'is_authenticated': request.user.is_authenticated, 'error': '403', 'title': 'Bad Request', 'desc': 'An error occured loading this page, if you believe this is an error, please contact the site administrator.'})
    return render(request, 'atc_site//error.html', {'user': request.user, 'is_authenticated': request.user.is_authenticated, 'error': '400', 'title': 'Forbidden Access', 'desc': 'You do not have permission to access this page. If you believe this is an error, please contact the site administrator.'})



@login_required
def create_item(request):
    if request.user.groups.filter(name='Vendor').exists():
        if request.method == 'POST':
            print(request.POST['name'].lower())
        return render(request, 'atc_site//vendor//create_item.html', {'title': 'Create Item', 'user': request.user, 'is_authenticated': request.user.is_authenticated, 'vendor': request.user})
    return render(request, 'atc_site//error.html', {'user': request.user, 'is_authenticated': request.user.is_authenticated, 'error': '400', 'title': 'Forbidden Access', 'desc': 'You do not have permission to access this page. If you believe this is an error, please contact the site administrator.'})

@login_required
def edit_item(request, item_id):
    if request.user.groups.filter(name='Vendor').exists():
        #handle the POST request -> if request.POST:
        try:
            item = FoodAndDrinksItem.objects.get(id=item_id)
            if request.user == item.vendor: return render(request, 'atc_site//vendor//edit_item.html', {'title': 'Edit Item', 'user': request.user, 'is_authenticated': request.user.is_authenticated, 'vendor': request.user, 'item': item})
        except: return render(request, 'atc_site//error.html', {'user': request.user, 'is_authenticated': request.user.is_authenticated, 'error': '403', 'title': 'Bad Request', 'desc': 'An error occured loading this page, if you believe this is an error, please contact the site administrator.'})
    return render(request, 'atc_site//error.html', {'user': request.user, 'is_authenticated': request.user.is_authenticated, 'error': '400', 'title': 'Forbidden Access', 'desc': 'You do not have permission to access this page. If you believe this is an error, please contact the site administrator.'})

@login_required
def delete_item(request, item_id):
    if request.user.groups.filter(name='Vendor').exists():
        try:
            item = FoodAndDrinksItem.objects.get(id=item_id)
            if request.user == item.vendor: 
                item.delete()
                return redirect('/vendor/dashboard/items/')
        except: return render(request, 'atc_site//error.html', {'user': request.user, 'is_authenticated': request.user.is_authenticated, 'error': '403', 'title': 'Bad Request', 'desc': 'An error occured loading this page, if you believe this is an error, please contact the site administrator.'})
    return render(request, 'atc_site//error.html', {'user': request.user, 'is_authenticated': request.user.is_authenticated, 'error': '400', 'title': 'Forbidden Access', 'desc': 'You do not have permission to access this page. If you believe this is an error, please contact the site administrator.'})

def get_vendor_orders(vendor):
    """
    Get all orders for a given vendor.
    """
    items = EventFoodAndDrinks.objects.filter(food_and_drinks_item__vendor=vendor).all()
    vendor_orders = []
    for item in items:
        food_and_drinks = FoodAndDrinks.objects.filter(item=item)
        for food_and_drink in food_and_drinks:
            vendor_orders.append(food_and_drink)
        
    
    return vendor_orders