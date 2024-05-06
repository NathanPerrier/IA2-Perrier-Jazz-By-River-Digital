import os
from django.contrib.auth import authenticate, login
from django.shortcuts import render
from django.http import StreamingHttpResponse, JsonResponse
from django.conf import settings
from django.core.cache import cache
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import logout
from decouple import config
import stripe

stripe.api_key = config('STRIPE_API_KEY')

from ...main import *
from ...atc.main import register_page as register_page_atc
from ...weather_app.main import register_page as register_page_weather
from ...atc.main import *
from ....models import CustomUser, CustomUserManager
from allauth.account.models import EmailAddress
from ...auth.register.models import RegisterAuth

def register_get_email_view(request, error=''):
    '''
    This function handles the GET request for the register page. If the request method is POST, it calls the 'create_and_send_reset_code' method of the 'RegisterAuth' model to create a new entry with the provided email, first name, and last name. It then sends a registration code to the user's email address. The function returns a JSON response with a success flag and an error message if applicable. If the request method is not POST, it renders the register page based on the path ('weather' or 'atc').

    Parameters:
    - request: The HTTP request object.
    - error (optional): A string representing an error message.

    Returns:
    - If the request method is POST, it returns a JSON response with a success flag and an error message (if applicable).
    - If the request method is not POST, it renders the register page based on the path ('weather' or 'atc').

    '''
    if request.method == 'POST':
        success, error = RegisterAuth.create_and_send_reset_code(request.POST['first_name'], request.POST['last_name'], request.POST['email'].lower())
        return JsonResponse({'success': success, 'error': error})
    return register_page_weather(request) if 'weather' in request.path else register_page_atc(request)

def register_get_code_view(request):    
    '''
    View function for registering a user and generating a verification code.

    Parameters:
    - request: The HTTP request object.

    Returns:
    - If the request method is POST, returns a JsonResponse with the success status and error message (if any).
    - If the request method is not POST, returns the rendered register page for either the weather app or ATC, based on the request path.

    '''
    if request.method == 'POST':
        success, error = RegisterAuth.check_code_entry(request.POST['email'].lower(), request.POST['code'])
        return JsonResponse({'success': success, 'error': error})
    return register_page_weather(request) if 'weather' in request.path else register_page_atc(request)

def register_set_password_view(request):
    """
    Register a user with a password and perform additional actions.

    This function is responsible for registering a user with a password and performing additional actions such as creating a Stripe customer, logging in the user, and returning a JSON response indicating success.

    Parameters:
        request (HttpRequest): The HTTP request object.

    Returns:
        JsonResponse: A JSON response indicating the success of the registration process.

    Example:
        >>> register_set_password_view(request)
        {'success': True, 'error': ''}
    """
    if request.method == 'POST':
        user = CustomUser.objects.check_user(first_name=request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email'].lower(), password=request.POST['password'])
        email = EmailAddress(user=user, email=user.email, primary=True, verified=True)
        email.save()
        create_stripe_customer(user)
        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        return JsonResponse({'success': True, 'error': ''})
    return register_page_weather(request) if 'weather' in request.path else register_page_atc(request)   

def create_stripe_customer(user):
    """
        Creates a Stripe customer for the given user.
    """
    stripe.Customer.create(
        id=f'customuser-{str(user.id)}',
        name=str(user.first_name + ' ' + user.last_name),
        email=user.email,
    )