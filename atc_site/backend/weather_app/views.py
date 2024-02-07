import os
from django.shortcuts import render
from django.http import StreamingHttpResponse, JsonResponse
from django.conf import settings
from django.core.cache import cache
from decouple import config
from django.views.decorators.http import require_POST
from django.contrib.auth import logout
import urllib.parse
import re

from .main import *
from .weather.main import RetrieveWeather

def search_location(request, location):
    if location:
        print('location:', location)
        try: locationData=split_location(location)
        except: return search(request, error='Invalid locationData')   
        print('locationData:', locationData)
        try:
            model = RetrieveWeather(locationData)
            locationData = model.request.location()
            print('locationData:', locationData)
        
            if not locationData and 'Home' not in urllib.parse.unquote(location): return search(request, error='Invalid Location')
            
            print('locationData:', locationData)
            locationDict = {
                'city': locationData['name'], 
                'timezone': locationData['timezone'], 
                'country': locationData['timezone'].split('/')[0], 
                'lat': locationData['latitude'], 
                'lon': locationData['longitude']
            }
        except Exception as e: 
            print(e)
            return render(request, 'landing-error.html', {'tomorrowio_api_key': config("TOMORROWIO_API_KEY"), 'is_authenticated': request.user.is_authenticated})
        
        if not locationData: return search(request, error='Invalid Location')
        
        try: 
            return render(request, 'landing.html', {'is_authenticated': request.user.is_authenticated, 'location': locationDict, 'image': GenerateLocationImage(city=locationData['name'], region=locationData['state'], country=locationData['timezone'].split('/')[0], lat=locationData['latitude'], lon=locationData['longitude']).get_image(), 'forecast_daily': model.Forecast(model.request).get_daily(), 'forecast_hourly': model.Forecast(model.request).get_hourly(), 'mapbox_access_token': config('MAPBOX_ACCESS_TOKEN'), 'tomorrowio_api_key': config("TOMORROWIO_API_KEY"), 'hervey_bay': (lambda model: model.Forecast(model.request).get_hourly())(RetrieveWeather('4655')), 'perth': (lambda model: model.Forecast(model.request).get_hourly())(RetrieveWeather('6000')), 'sydney': (lambda model: model.Forecast(model.request).get_hourly())(RetrieveWeather('2000')), 'gold_coast': (lambda model: model.Forecast(model.request).get_hourly())(RetrieveWeather('4217')), 'melbourne': (lambda model: model.Forecast(model.request).get_hourly())(RetrieveWeather('3000')), 'warning': model.Warnings(model.request).get_warnings()})
        except: return render(request, 'landing-error.html', {'tomorrowio_api_key': config("TOMORROWIO_API_KEY"), 'is_authenticated': request.user.is_authenticated})  
    return search(request, error='Invalid Location')
    


    
@require_POST
def get_user_location(request):
    if request.method == 'POST':
        print(request.POST['latitude'], request.POST['longitude'])
        cache.set('latitude', request.POST['latitude'])
        cache.set('longitude', request.POST['longitude'])
        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False})


def split_location(location):
    
    # List of Australian state abbreviations
    states = ['ACT', 'NSW', 'NT', 'QLD', 'SA', 'TAS', 'VIC', 'WA']

    # Create a regular expression pattern that matches any of the state abbreviations
    pattern = '|'.join(states)
    
    location = urllib.parse.unquote(location)
    
    location = re.split(',', location)[0]

    # Split the location at the state abbreviation
    location_parts = re.split(pattern, location)

    # The first part of the split location is the city
    city = location_parts[0].strip()
    
    city = city.replace(' ', '+')

    return city