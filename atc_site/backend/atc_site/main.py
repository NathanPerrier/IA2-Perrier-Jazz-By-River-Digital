from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_POST

from .subjects import *
from .terms import *

def index(request):
    return render(request, 'atc_site//index.html')

def erea(request):
    return render(request, 'atc_site//erea.html')

def subjects(request):
    return render(request, 'atc_site//subjects.html')

def terms(request):
    return render(request, 'atc_site//terms and policies.html')

@require_POST
#@handle_newsletter
def handle_newsletter(request):
    return JsonResponse({'success': True, 'error': None}, status=200)

@require_POST
#@handle_contact_request
def handle_contact_request():
    return JsonResponse({'success': True, 'error': None}, status=200)