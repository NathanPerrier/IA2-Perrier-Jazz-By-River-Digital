from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_protect

from ..events.booking.models import Booking
from ..events.food_and_drinks.models import FoodAndDrinksItem, EventFoodAndDrinks, BookingFoodAndDrinks
from ..events.vouchers.models import Voucher, EventVoucher, BookingVouchers
from django.contrib.auth.models import Group

def account_page(request):
    print(request.user.is_authenticated)
    if request.user.is_authenticated:
        return render(request, 'atc_site/account//account.html', {'user': request.user, 'is_authenticated': request.user.is_authenticated, 'user_group': [group.name for group in Group.objects.filter(customuser=request.user)][0], 'bookings': Booking().get_bookings_by_user(request.user.id), 'booking_food_and_drinks': (True if [(food_and_drinks.booking in [booking for booking in Booking().get_bookings_by_user(request.user.id)]) for food_and_drinks in BookingFoodAndDrinks.objects.filter(user=request.user).all()] else False), 'booking_vouchers': (True if [(voucher.booking in [booking for booking in Booking().get_bookings_by_user(request.user.id)]) for voucher in BookingVouchers.objects.filter(user=request.user).all()] else False)})
    else: return redirect('/login')
   
@csrf_protect
def manage_account_page(request):
    if request.user.is_authenticated:
        return render(request, 'atc_site/account/manage_account.html', {'user': request.user, 'is_authenticated': request.user.is_authenticated, 'user_group': [group.name for group in Group.objects.filter(customuser=request.user)][0]})
    else: return redirect('/login')