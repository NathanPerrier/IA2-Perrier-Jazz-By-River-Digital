"""URLs for the booking app."""
from django.urls import path

from . import views


urlpatterns = [
  path('<int:booking_id>/', views.booking_view, name='booking_view')
]
