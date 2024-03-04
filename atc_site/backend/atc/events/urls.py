from django.contrib import admin
from django.urls import include, path
from . import main
from . import views

urlpatterns = [
    path("", main.events, name="events"),
    
    path('booking/', include('atc_site.backend.atc.events.booking.urls')),
]