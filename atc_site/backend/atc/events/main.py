from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_protect
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import Group
from .models import Events, EventSchedule, EventScheduleItem
from .food_and_drinks.models import FoodAndDrinks, FoodAndDrinksItem, EventFoodAndDrinks
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
    return render(request, 'atc_site//events//event.html', {'user': request.user, 'is_authenticated': request.user.is_authenticated, 'event' : Events.objects.get(id=event_id), 'days_to_go': days_to_go(Events.objects.get(id=event_id).date, datetime.datetime.now()), 'schedule': get_event_schedule(event_id), 'food_and_drinks': get_event_food_and_drinks(event_id)})

@staff_member_required
def edit_event(request, event_id):
    if request.user.is_superuser:
        return render(request, 'atc_site//events//edit.html', {'user': request.user, 'is_authenticated': request.user.is_authenticated, 'google_places_api_key': config('GOOGLE_PLACES_API_KEY')})
    return render(request, 'atc_site//error.html', {'user': request.user, 'is_authenticated': request.user.is_authenticated, 'error' : '403', 'title' : 'Access Forbidden', 'desc' : 'You do not have permission to access this page. Please contact the administrator if you believe this is an error.'})


def days_to_go(date1, date2):
    date1 = date1.replace(tzinfo=None)
    date2 = date2.replace(tzinfo=None)
    return abs((date2 - date1).days)

def get_event_schedule(event_id):
    event_schedule = EventSchedule.objects.filter(event=event_id)
    schedule_items = []
    for schedule in event_schedule:
        items = EventScheduleItem.objects.filter(id=schedule.event_item.id)
        for item in items:
            schedule_items.append({
                'start_time': item.start_time,
                'end_time': item.end_time,
                'title': item.title,
                'description': item.description,
                'creation_time': item.creation_time,
                'last_modified': item.last_modified,
            })
    return schedule_items

def get_event_food_and_drinks(event_id):
    food_and_drinks = EventFoodAndDrinks.objects.filter(event=event_id)
    food_and_drinks_items = []
    for food_and_drink in food_and_drinks:
        items = FoodAndDrinksItem.objects.filter(id=food_and_drink.food_and_drinks_item.id)
        for item in items:
            food_and_drinks_items.append({
                'name': item.name,
                'description': item.description,
                'price': item.price,
                'vemdor': item.vendor,
                'stock': item.stock,
                'image': item.image,
            })
    return food_and_drinks_items