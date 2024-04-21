from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_protect
import stripe
from decouple import config

stripe.api_key = config('STRIPE_API_KEY')

from ..events.booking.models import Booking
from ..events.food_and_drinks.models import FoodAndDrinksItem, EventFoodAndDrinks, BookingFoodAndDrinks
from ..events.vouchers.models import Voucher, EventVoucher, BookingVouchers
from django.contrib.auth.models import Group

def account_page(request):
    if request.user.is_authenticated:
        return render(request, 'atc_site/account//account.html', {'user': request.user, 'is_authenticated': request.user.is_authenticated, 'user_group': [group.name for group in Group.objects.filter(customuser=request.user)][0], 'bookings': Booking().get_bookings_by_user(request.user.id), 'food_and_drinks_booking': check_queryset(Booking.objects.filter(user=request.user), BookingFoodAndDrinks.objects.all()), 'vouchers_booking': check_queryset(Booking.objects.filter(user=request.user), BookingVouchers.objects.all())})
    else: return redirect('/login')
   
@csrf_protect
def manage_account_page(request):
    if request.user.is_authenticated:
        return render(request, 'atc_site/account/manage_account.html', {'user': request.user, 'is_authenticated': request.user.is_authenticated, 'user_group': [group.name for group in Group.objects.filter(customuser=request.user)][0], 'stripe_customer': stripe.Customer.retrieve(f'customuser-{request.user.id}')})
    else: return redirect('/login')
    
def check_queryset(bookings, queryset):
    bookingExtras = []
    for item in queryset:
        if item.booking in bookings and item.booking not in bookingExtras:
            bookingExtras.append(item.booking)
    print(bookingExtras)
    return bookingExtras

