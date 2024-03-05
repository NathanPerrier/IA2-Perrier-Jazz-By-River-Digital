from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_protect
from django.contrib.admin.views.decorators import staff_member_required
from decouple import config


def events(request):
    return render(request, 'atc_site//events//events.html', {'user': request.user, 'is_authenticated': request.user.is_authenticated})

@staff_member_required
def create_event(request):
    if request.user.is_superuser:
        return render(request, 'atc_site//events//create.html', {'user': request.user, 'is_authenticated': request.user.is_authenticated, 'google_places_api_key': config('GOOGLE_PLACES_API_KEY')})
    return render(request, 'atc_site//error.html', {'user': request.user, 'is_authenticated': request.user.is_authenticated, 'error' : '403', 'title' : 'Access Forbidden', 'desc' : 'You do not have permission to access this page. Please contact the administrator if you believe this is an error.'})



@staff_member_required
def edit_event(request, event_id):
    if request.user.is_superuser:
        return render(request, 'atc_site//events//edit.html', {'user': request.user, 'is_authenticated': request.user.is_authenticated, 'google_places_api_key': config('GOOGLE_PLACES_API_KEY')})
    return render(request, 'atc_site//error.html', {'user': request.user, 'is_authenticated': request.user.is_authenticated, 'error' : '403', 'title' : 'Access Forbidden', 'desc' : 'You do not have permission to access this page. Please contact the administrator if you believe this is an error.'})

