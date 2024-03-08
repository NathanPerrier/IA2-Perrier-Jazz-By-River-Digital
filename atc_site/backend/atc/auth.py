from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_protect

@csrf_protect
def login_page(request, error=''):
    return render(request, 'atc_site//login.html', {'error': error, 'range_25': range(25)}) #'google_maps_api_key': config("GOOGLE_MAPS_API_KEY")

@csrf_protect
def register_page(request, error=''):
    return render(request, 'atc_site//register.html', {'error': error, 'range_25': range(25)}) #'google_maps_api_key': config("GOOGLE_MAPS_API_KEY")

@csrf_protect
def forgot_password_page(request, error=''):
    return render(request, 'atc_site//forgot_password.html', {'error': error, 'range_25': range(25)})