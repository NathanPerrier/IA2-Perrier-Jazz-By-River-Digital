from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_protect

from ..events.booking.models import Booking
from django.contrib.auth.models import Group

def account_page(request):
    print(request.user.is_authenticated)
    if request.user.is_authenticated:
        return render(request, 'atc_site/account//account.html', {'user': request.user, 'is_authenticated': request.user.is_authenticated, 'user_group': [group.name for group in Group.objects.filter(customuser=request.user)][0], 'bookings': Booking().get_bookings_by_user(request.user.id)})
    else: return redirect('/login')
   