from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_protect

def events(request):
    return render(request, 'atc_site//events//events.html', {'user': request.user, 'is_authenticated': request.user.is_authenticated})