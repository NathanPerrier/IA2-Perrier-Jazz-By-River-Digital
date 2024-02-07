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
from .auth.views import *
from .atc.main import *
# from .weather.main import RetrieveWeather

def register_view(request):
    return register_page(request)
    
def forgot_password_view(request):
    return forgot_password_page(request)

def logout_view(request):
    logout(request)
    return index(request)
    
def stream_video(request, video_path):
    video_path = os.path.join(settings.BASE_DIR, 'atc_site/frontend/static/videos', video_path)
    def play_video(video_path):
        with open(video_path, 'rb') as video:
            for chunk in iter(lambda: video.read(4096), b""):
                yield chunk

    response = StreamingHttpResponse(play_video(video_path))
    response['Content-Type'] = 'video/mp4'
    return response


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