
from django.conf import settings
from django.conf.urls.static import static

from django.contrib.auth import views as auth_views
from django.contrib import admin
from django.urls import include, path
from . import main, views
from .chatbot.views import chat
from atc_site.backend import views as atc_views

urlpatterns = [   
    path("", main.index, name="index"),
    path("radar", main.radar, name="radar"),
    path("routes", main.routes, name="routes"),
    path("search", main.search, name="search"),
    path("search/<str:location>", views.search_location, name="search_location"),
    path("saved", main.saved, name="saved"),
    path("search/", main.search, name="search"),
    
    path('login', atc_views.loginViewWeather, name='login'),
    
    path('register/', views.register_view, name='register'),
    path('register/get_email/', atc_views.register_get_email_view, name='register_get_email'),
    path('register/get_code/', atc_views.register_get_code_view, name='register_get_code'),
    path('register/set_password/', atc_views.register_set_password_view, name='register_set_password'),
    
    path('forgot/', views.forgot_password_view, name='forgot_password'),
    path('forgot/get_email/', atc_views.forgot_password_get_email_view, name='forgot_password_get_email'),
    path('forgot/get_code/', atc_views.forgot_password_get_code_view, name='forgot_password_get_code'),
    path('forgot/set_password/', atc_views.forgot_password_set_password_view, name='forgot_password_set_password'),
    
    
    path("", include("atc_site.backend.weather_app.chatbot.urls"), name="chatbot"),
]