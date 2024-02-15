from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from decouple import config

from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from decouple import config

from ..location.main import *
from .weather.main import RetrieveWeather
from .locationImage.Dalle3.main import GenerateLocationImage

@csrf_protect
def index(request):
    try:
        location = GetLocation().get_location()
        print(location)
        model = RetrieveWeather(location.zip)
        if location and model:
            return render(request, 'landing.html', {'is_authenticated': request.user.is_authenticated, 'location': location, 'image': GenerateLocationImage(location=location).get_image(), 'forecast_daily': model.Forecast(model.request).get_daily(), 'forecast_hourly': model.Forecast(model.request).get_hourly(), 'mapbox_access_token': config('MAPBOX_ACCESS_TOKEN'), 'tomorrowio_api_key': config("TOMORROWIO_API_KEY"), 'hervey_bay': (lambda model: model.Forecast(model.request).get_hourly())(RetrieveWeather('Hervey+Bay')), 'perth': (lambda model: model.Forecast(model.request).get_hourly())(RetrieveWeather('6000')), 'sydney': (lambda model: model.Forecast(model.request).get_hourly())(RetrieveWeather('2000')), 'gold_coast': (lambda model: model.Forecast(model.request).get_hourly())(RetrieveWeather('4217')), 'melbourne': (lambda model: model.Forecast(model.request).get_hourly())(RetrieveWeather('3000')), 'warning': model.Warnings(model.request).get_warnings()})  #* removed 'icon': GetWeatherIcon().get_weather_icon(), 'weather_desc': GetWeatherDescription(GetLocation().get_location()).get_weather_description()
        return render(request, 'landing-error.html', {'tomorrowio_api_key': config("TOMORROWIO_API_KEY"), 'is_authenticated': request.user.is_authenticated})
    except Exception as e:
        print('error:', e)
        return render(request, 'landing-error.html', {'tomorrowio_api_key': config("TOMORROWIO_API_KEY"), 'is_authenticated': request.user.is_authenticated})
    
def radar(request):
    return render(request, 'radar.html', {'tomorrowio_api_key': config("TOMORROWIO_API_KEY"), 'location': GetLocation().get_location(), 'is_authenticated': request.user.is_authenticated, 'mapbox_access_token': config('MAPBOX_ACCESS_TOKEN')}) #'google_maps_api_key': config("GOOGLE_MAPS_API_KEY")

def routes(request, start=None, end=None, mode=None):
    if start:
        return render(request, 'routes.html', {'tomorrowio_api_key': config("TOMORROWIO_API_KEY"), 'location': GetLocation().get_location(), 'is_authenticated': request.user.is_authenticated, 'mapbox_access_token': config('MAPBOX_ACCESS_TOKEN'), 'start': start, 'end': end, 'mode': mode})
    return render(request, 'routes.html', {'tomorrowio_api_key': config("TOMORROWIO_API_KEY"), 'location': GetLocation().get_location(), 'is_authenticated': request.user.is_authenticated, 'mapbox_access_token': config('MAPBOX_ACCESS_TOKEN')})

def search(request, error=''):
    return render(request, 'search.html', {'tomorrowio_api_key': config("TOMORROWIO_API_KEY"), 'location': GetLocation().get_location(), 'is_authenticated': request.user.is_authenticated, 'google_places_api_key': config('GOOGLE_PLACES_API_KEY'), 'error': error})

def saved(request):
    if request.user.is_authenticated:
        return render(request, 'saved.html', {'tomorrowio_api_key': config("TOMORROWIO_API_KEY"), 'location': GetLocation().get_location(), 'is_authenticated': request.user.is_authenticated})
    else:
        return render(request, 'saved-error.html', {'tomorrowio_api_key': config("TOMORROWIO_API_KEY"), 'location': GetLocation().get_location(), 'is_authenticated': request.user.is_authenticated})
    



@csrf_protect
def login_page(request, error=''):
    return render(request, 'login.html', {'tomorrowio_api_key': config("TOMORROWIO_API_KEY"), 'location': GetLocation().get_location(), 'is_authenticated': request.user.is_authenticated, 'mapbox_access_token': config('MAPBOX_ACCESS_TOKEN'), 'error': error}) #'google_maps_api_key': config("GOOGLE_MAPS_API_KEY")

@csrf_protect
def register_page(request, error=''):
    return render(request, 'register.html', {'tomorrowio_api_key': config("TOMORROWIO_API_KEY"), 'location': GetLocation().get_location(), 'is_authenticated': request.user.is_authenticated, 'mapbox_access_token': config('MAPBOX_ACCESS_TOKEN'), 'error': error}) #'google_maps_api_key': config("GOOGLE_MAPS_API_KEY")

@csrf_protect
def forgot_password_page(request, error=''):
    return render(request, 'forgot_password.html', {'tomorrowio_api_key': config("TOMORROWIO_API_KEY"), 'location': GetLocation().get_location(), 'is_authenticated': request.user.is_authenticated, 'mapbox_access_token': config('MAPBOX_ACCESS_TOKEN'), 'error': error})