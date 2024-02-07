
from django.conf import settings
from django.conf.urls.static import static

from django.contrib.auth import views as auth_views
from django.contrib import admin
from django.urls import include, path
from . import main, views
from .chatbot.views import chat

urlpatterns = [   
    path("", main.index, name="index"),
    path("radar", main.radar, name="radar"),
    path("routes", main.routes, name="routes"),
    path("search", main.search, name="search"),
    path("search/<str:location>", views.search_location, name="search_location"),
    path("saved", main.saved, name="saved"),
    path("search/", main.search, name="search"),
    
    path("", include("atc_site.backend.weather_app.chatbot.urls"), name="chatbot"),
]