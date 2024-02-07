from django.shortcuts import render
from django.http import HttpResponseBadRequest, HttpResponseForbidden, HttpResponseNotFound, HttpResponseServerError, HttpResponseNotAllowed 

def handler400(request):
    context = {'title': 'Bad Request', 'error': '400', 'desc': 'There was an issue processing your request. This could be due to an invalid action or input. Please try again or return home.'}
    return HttpResponseBadRequest(request, 'atc_site//error.html', context, status=400)

def handler404(request):
    context = {'title': 'Page Not Found', 'error': '404', 'desc': 'We’re sorry, the page you have looked for does not exist in our website! Maybe go back to our home page or user the navigation bar?'}
    response =  render(request, 'atc_site//error.html', context, status=404)
    response.status_code = 404
    return response

def handler500(request):
    context = {'title': 'Internal Server Error', 'error': '500', 'desc': 'There is an error in loading the sever. Plase try again later.'}
    return HttpResponseServerError(request, 'atc_site//error.html', context, status=500)

def handler401(request):
    context = {'title': 'Unauthorized', 'error': '401', 'desc': 'You are not authorized to view this page. Please try again or return home.'}
    return HttpResponseNotAllowed(request, 'atc_site//error.html', context, status=401)

def handler403(request):
    context = {'title': 'Forbidden', 'error': '403', 'desc': 'You are not allowed to view this page. Please try again or return home.'}
    return HttpResponseForbidden(request, 'atc_site//error.html', context, status=403)