import os
from django.contrib.auth import authenticate, login
from django.shortcuts import render
from django.http import StreamingHttpResponse, JsonResponse
from django.conf import settings
from django.core.cache import cache
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import logout

from ...main import *
from ...atc.main import *
from ...atc.main import forgot_password_page as forgot_password_page_atc
from ...weather_app.main import forgot_password_page as forgot_password_page_weather
from ....models import CustomUser, CustomUserManager
from ...auth.forgot_password.models import ForgotPasswordAuth

def forgot_password_get_email_view(request, error=''):
    if request.method == 'POST':
        success, error = ForgotPasswordAuth.create_and_send_reset_code(request.POST['email'].lower())
        return JsonResponse({'success': success, 'error': error})
    return forgot_password_page_weather(request) if 'weather' in request.path else forgot_password_page_atc

def forgot_password_get_code_view(request):    
    if request.method == 'POST':
        print(request.POST['email'], request.POST['code'])
        success, error = ForgotPasswordAuth.check_code_entry(request.POST['email'].lower(), request.POST['code'])
        return JsonResponse({'success': success, 'error': error})
    return forgot_password_page_weather(request) if 'weather' in request.path else forgot_password_page_atc

def forgot_password_set_password_view(request):
    if request.method == 'POST':
        user = CustomUserManager().update_password(email=request.POST['email'].lower(), password=request.POST['password'])
        print(user)
        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        ForgotPasswordAuth().delete_by_user_id(user)
        return JsonResponse({'success': True, 'error': ''})
    return forgot_password_page_weather(request) if 'weather' in request.path else forgot_password_page_atc(request)