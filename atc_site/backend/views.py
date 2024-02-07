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
from .atc_site.main import *
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

