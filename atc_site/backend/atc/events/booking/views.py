"""Views for the booking app."""
from django.contrib.auth.decorators import login_required
from django.contrib.sessions.models import Session
from django.http import Http404
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, DetailView, ListView

from .models import Booking

def booking_view(request, booking_id):
    """View for a single booking."""
    try:
        booking = Booking.objects.get(id=booking_id)
    except Booking.DoesNotExist:
        raise render(request, 'atc_site/error.html', {'user': request.user, 'is_authenticated': request.user.is_authenticated, 'error': '404', 'title': 'Not Found', 'desc': 'The booking you are looking for does not exist.'})
    return render(request, 'atc_site/booking/booking.html', {'user': request.user, 'is_authenticated': request.user.is_authenticated, 'booking': booking})