from django.contrib import admin
from django.urls import include, path
from . import main
from . import views

urlpatterns = [
    path("", main.events, name="events"),
    path("<int:event_id>/", main.view_event, name="events"),
    
    path('booking/', include('atc_site.backend.atc.events.booking.urls')),
    
    path('create/', main.create_event, name='events'),
    path('<int:event_id>/edit/', main.edit_event, name='events'),
]