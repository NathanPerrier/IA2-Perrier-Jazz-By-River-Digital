from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_protect
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import Group
from .models import Events
from decouple import config
import datetime

from ....handles import login_required

def events(request):
    return render(request, 'atc_site//events//events.html', {'user': request.user, 'is_authenticated': request.user.is_authenticated, 'events' : Events.objects.all() })

@staff_member_required  #! redirects to /accounts/login
def create_event(request):
    if request.user.is_superuser:
        return render(request, 'atc_site//events//create.html', {'user': request.user, 'is_authenticated': request.user.is_authenticated, 'google_places_api_key': config('GOOGLE_PLACES_API_KEY')}) #, 'vendors': Group.objects.get(name='Vendors').user_set.all()
    return render(request, 'atc_site//error.html', {'user': request.user, 'is_authenticated': request.user.is_authenticated, 'error' : '403', 'title' : 'Access Forbidden', 'desc' : 'You do not have permission to access this page. Please contact the administrator if you believe this is an error.'})


def view_event(request, event_id):
    return render(request, 'atc_site//events//event.html', {'user': request.user, 'is_authenticated': request.user.is_authenticated, 'event' : Events.objects.get(id=event_id), 'days_to_go': days_to_go(Events.objects.get(id=event_id).date, datetime.datetime.now())})

@staff_member_required
def edit_event(request, event_id):
    if request.user.is_superuser:
        return render(request, 'atc_site//events//edit.html', {'user': request.user, 'is_authenticated': request.user.is_authenticated, 'google_places_api_key': config('GOOGLE_PLACES_API_KEY')})
    return render(request, 'atc_site//error.html', {'user': request.user, 'is_authenticated': request.user.is_authenticated, 'error' : '403', 'title' : 'Access Forbidden', 'desc' : 'You do not have permission to access this page. Please contact the administrator if you believe this is an error.'})


def days_to_go(date1, date2):
    date1 = date1.replace(tzinfo=None)
    date2 = date2.replace(tzinfo=None)
    return abs((date2 - date1).days)