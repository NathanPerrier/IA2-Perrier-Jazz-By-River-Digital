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
from ....models import CustomUser, CustomUserManager
from ...auth.register.models import RegisterAuth

def register_get_email_view(request, error=''):
    if request.method == 'POST':
        success, error = RegisterAuth.create_and_send_reset_code(request.POST['first_name'], request.POST['last_name'], request.POST['email'])
        return JsonResponse({'success': success, 'error': error})
    return register_page(request)

def register_get_code_view(request):    
    if request.method == 'POST':
        success, error = RegisterAuth.check_code_entry(request.POST['email'], request.POST['code'])
        return JsonResponse({'success': success, 'error': error})
    return register_page(request)

def register_set_password_view(request):
    if request.method == 'POST':
        user = CustomUser.objects.create_user(first_name=request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email'], password=request.POST['password'])
        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        return JsonResponse({'success': True, 'error': ''})
    return register_page(request)    