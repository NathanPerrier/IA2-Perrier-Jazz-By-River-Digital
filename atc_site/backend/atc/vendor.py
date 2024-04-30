import stripe
from decouple import config
from django.contrib.auth.decorators import login_required
from .main import *
from django.db.models import Count
from django.utils import timezone
import time, datetime, calendar
from .events.food_and_drinks.models import FoodAndDrinksItem, FoodAndDrinks, BookingFoodAndDrinks, EventFoodAndDrinks

stripe.api_key = config('STRIPE_API_KEY')

@login_required
def vendor_dashboard(request):
    if request.user.groups.filter(name='Vendor').exists():
        return render(request, 'atc_site//vendor//vendor_dashboard.html', {'title': 'Vendor Dashboard', 'user': request.user, 'is_authenticated': request.user.is_authenticated, 'vendor': request.user, 'customers': get_customer(request.user), 'revenue': get_revenue(request.user), 'active_orders': get_active_orders(request.user), 'revenue_for_each_month': get_revenue_for_each_month(request.user), 'revenue_by_customer': get_revenue_by_customer(request.user), 'top_selling_items': get_top_5_selling_items(request.user)})
    return render(request, 'atc_site//error.html', {'user': request.user, 'is_authenticated': request.user.is_authenticated, 'error': '400', 'title': 'Forbidden Access', 'desc': 'You do not have permission to access this page. If you believe this is an error, please contact the site administrator.'})

@login_required
def vendor_items(request):
    if request.user.groups.filter(name='Vendor').exists():
        return render(request, 'atc_site//vendor//manage_items.html', {'title': 'Manage Items', 'user': request.user, 'is_authenticated': request.user.is_authenticated, 'vendor': request.user, 'items': FoodAndDrinksItem.objects.filter(vendor=request.user).all(), 'active_items': get_active_items(request.user)})
    return render(request, 'atc_site//error.html', {'user': request.user, 'is_authenticated': request.user.is_authenticated, 'error': '400', 'title': 'Forbidden Access', 'desc': 'You do not have permission to access this page. If you believe this is an error, please contact the site administrator.'})

# @login_required
# def vendor_item(request, item_id):
#     if request.user.groups.filter(name='Vendor').exists():
#         try:
#             item = FoodAndDrinksItem.objects.get(id=item_id)
#             if request.user == item.vendor: return render(request, 'atc_site//vendor//view_item.html', {'title': 'Edit Item', 'user': request.user, 'is_authenticated': request.user.is_authenticated, 'vendor': request.user, 'item': item})
#         except: return render(request, 'atc_site//error.html', {'user': request.user, 'is_authenticated': request.user.is_authenticated, 'error': '403', 'title': 'Bad Request', 'desc': 'An error occured loading this page, if you believe this is an error, please contact the site administrator.'})
#     return render(request, 'atc_site//error.html', {'user': request.user, 'is_authenticated': request.user.is_authenticated, 'error': '400', 'title': 'Forbidden Access', 'desc': 'You do not have permission to access this page. If you believe this is an error, please contact the site administrator.'})



@login_required  
def vendor_orders(request):
    if request.user.groups.filter(name='Vendor').exists():
        try:
            #get items from FoodandDrinks where item.item.vendor is request.user
            orders = get_vendor_orders(request.user)
            return render(request, 'atc_site//vendor//manage_orders.html', {'title': 'Manage Orders', 'user': request.user, 'is_authenticated': request.user.is_authenticated, 'vendor': request.user, 'orders': orders, 'booking_orders': BookingFoodAndDrinks.objects.all()})
        except: return render(request, 'atc_site//error.html', {'user': request.user, 'is_authenticated': request.user.is_authenticated, 'error': '403', 'title': 'Bad Request', 'desc': 'An error occured loading this page, if you believe this is an error, please contact the site administrator.'})
    return render(request, 'atc_site//error.html', {'user': request.user, 'is_authenticated': request.user.is_authenticated, 'error': '400', 'title': 'Forbidden Access', 'desc': 'You do not have permission to access this page. If you believe this is an error, please contact the site administrator.'})

@login_required
def vendor_order(request, order_id):
    if request.user.groups.filter(name='Vendor').exists():
        try:
            order = FoodAndDrinks.objects.get(id=order_id)
            booking_order = BookingFoodAndDrinks.objects.get(food_and_drinks=order)
            payment_intent = stripe.PaymentIntent.retrieve(booking_order.booking.payment.stripe_payment_id)
            if order.item.food_and_drinks_item.vendor == request.user: return render(request, 'atc_site//vendor//manage_order.html', {'title': 'Vendor Order', 'user': request.user, 'is_authenticated': request.user.is_authenticated, 'vendor': request.user, 'order': order, 'booking_order': booking_order, 'payment_intent': payment_intent, 'invoice': stripe.Invoice.retrieve(booking_order.booking.stripe_invoice_id), 'payment_method': stripe.PaymentMethod.retrieve(payment_intent.payment_method), 'vendor_items': get_names_of_items(request.user), 'customer': stripe.Customer.retrieve(f'customuser-{booking_order.booking.user.id}')})
        except Exception as e:
            print(e)
            return render(request, 'atc_site//error.html', {'user': request.user, 'is_authenticated': request.user.is_authenticated, 'error': '403', 'title': 'Bad Request', 'desc': 'An error occured loading this page, if you believe this is an error, please contact the site administrator.'})
    return render(request, 'atc_site//error.html', {'user': request.user, 'is_authenticated': request.user.is_authenticated, 'error': '400', 'title': 'Forbidden Access', 'desc': 'You do not have permission to access this page. If you believe this is an error, please contact the site administrator.'})



@login_required
def create_item(request):
    if request.user.groups.filter(name='Vendor').exists():
        if request.method == 'POST':
            print(request.POST['name'].capitalize())
            print('price', request.POST['price'])
            print('stock', request.POST['stock'])
            print('description', request.POST['description']) #! issue retrieving description (returns null)
            return JsonResponse({'success': True})
        return render(request, 'atc_site//vendor//create_item.html', {'title': 'Create Item', 'user': request.user, 'is_authenticated': request.user.is_authenticated, 'vendor': request.user})
    return render(request, 'atc_site//error.html', {'user': request.user, 'is_authenticated': request.user.is_authenticated, 'error': '400', 'title': 'Forbidden Access', 'desc': 'You do not have permission to access this page. If you believe this is an error, please contact the site administrator.'})

@login_required
def edit_item(request, item_id):
    if request.user.groups.filter(name='Vendor').exists():
        #handle the POST request -> if request.POST:
        if request.method == 'POST':
            print(request.POST['name'].capitalize())
            print('price', request.POST['price'])
            print('stock', request.POST['stock'])
            print('description', request.POST['description']) #! issue retrieving description (returns null)
            return JsonResponse({'success': True})
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

def get_names_of_items(vendor):
    """
    Get all names of items for a given vendor.
    """
    items = EventFoodAndDrinks.objects.filter(food_and_drinks_item__vendor=vendor).all()
    item_names = []
    for item in items:
        item_names.append(item.food_and_drinks_item.name)
        
    return item_names

def get_active_items(vendor):
    active_items = []
    items = EventFoodAndDrinks.objects.filter(food_and_drinks_item__vendor=vendor)
    
    for item in items:
        active_items.append(item.food_and_drinks_item)
        
    return active_items

def get_customer(vendor):
    """
    Get all customers for a given vendor.
    """
    items = BookingFoodAndDrinks.objects.filter(food_and_drinks__item__food_and_drinks_item__vendor=vendor).all()
    customers = []
    for item in items:
        if item.user not in customers:
            customers.append(item.user)
    return len(customers)

def get_revenue(vendor):
    revenue = 0
    items = BookingFoodAndDrinks.objects.filter(food_and_drinks__item__food_and_drinks_item__vendor=vendor).all()
    for item in items:
        revenue += item.food_and_drinks.quantity * item.food_and_drinks.item.food_and_drinks_item.price
    return revenue

def get_active_orders(vendor):
    """
    Get all active orders for a given vendor.
    """
    items = BookingFoodAndDrinks.objects.filter(food_and_drinks__item__food_and_drinks_item__vendor=vendor).all()
    active_orders = []
    for item in items:
        if item.booking.event.date > timezone.now():
            active_orders.append(item.food_and_drinks)
    return len(active_orders)

def get_revenue_for_each_month(vendor):
    """
    Get revenue for each month for a given vendor.
    """
    items = BookingFoodAndDrinks.objects.filter(food_and_drinks__item__food_and_drinks_item__vendor=vendor).all()
    revenue = {}
    for item in items:
        month = item.booking.event.date.strftime('%B')
        if month not in revenue:
            revenue[month] = 0
        revenue[month] += item.food_and_drinks.quantity * item.food_and_drinks.item.food_and_drinks_item.price
        
    if len(revenue) < 5:
        # Create a new dictionary to hold the new items
        new_items = {}
        for i in range(5-len(revenue)):
            new_items[calendar.month_name[datetime.datetime.now().month-(((5-1)-len(revenue))-i)]] = 0

        # Update the new_items dictionary with the existing revenue dictionary
        new_items.update(revenue)

        # Replace the revenue dictionary with the new_items dictionary
        revenue = new_items
    return revenue

def get_revenue_by_customer(vendor):
    """
    Get revenue by customer for a given vendor.
    """
    items = BookingFoodAndDrinks.objects.filter(food_and_drinks__item__food_and_drinks_item__vendor=vendor).all()
    revenue = {}
    for item in items:
        if item.user not in revenue and len(revenue) < 5:
            revenue[item.user] = 0
        revenue[item.user] += item.food_and_drinks.quantity * item.food_and_drinks.item.food_and_drinks_item.price
    return {k: v for k, v in sorted(revenue.items(), key=lambda item: item[1], reverse=True)}

def get_top_5_selling_items(vendor):
    """
    Get the top 5 selling items for a given vendor.
    """
    items = BookingFoodAndDrinks.objects.filter(food_and_drinks__item__food_and_drinks_item__vendor=vendor).all()
    top_items = {}
    for item in items:
        if item.food_and_drinks.item.food_and_drinks_item not in top_items:
            top_items[item.food_and_drinks.item.food_and_drinks_item] = 0
        top_items[item.food_and_drinks.item.food_and_drinks_item] += item.food_and_drinks.quantity*item.food_and_drinks.item.food_and_drinks_item.price
    return {k: v for k, v in sorted(top_items.items(), key=lambda item: item[1], reverse=True)[:5]}