from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_protect

from .subjects import *
from .terms import *


#* split into respective folders and files later on

def index(request):
    return render(request, 'atc_site//index.html', {'user': request.user, 'is_authenticated': request.user.is_authenticated})

def erea(request):
    return render(request, 'atc_site//erea.html', {'user': request.user, 'is_authenticated': request.user.is_authenticated})

def subjects(request):
    return render(request, 'atc_site//subjects.html', {'user': request.user, 'is_authenticated': request.user.is_authenticated})

def terms(request):
    return render(request, 'atc_site//terms and policies.html', {'user': request.user, 'is_authenticated': request.user.is_authenticated})

@csrf_protect
def login_page(request, error=''):
    return render(request, 'atc_site//login.html', {'error': error, 'range_25': range(25)}) #'google_maps_api_key': config("GOOGLE_MAPS_API_KEY")

@csrf_protect
def register_page(request, error=''):
    return render(request, 'atc_site//register.html', {'error': error, 'range_25': range(25)}) #'google_maps_api_key': config("GOOGLE_MAPS_API_KEY")

@csrf_protect
def forgot_password_page(request, error=''):
    return render(request, 'atc_site//forgot_password.html', {'error': error, 'range_25': range(25)})

def account_page(request):
    return render(request, 'atc_site/account//account.html', {'user': request.user, 'is_authenticated': request.user.is_authenticated})

@require_POST
#@handle_newsletter
def handle_newsletter(request):
    return JsonResponse({'success': True, 'error': None}, status=200)

@require_POST
#@handle_contact_request
def handle_contact_request():
    return JsonResponse({'success': True, 'error': None}, status=200)