"""Views for the booking app."""
from django.contrib.auth.decorators import login_required
from django.contrib.sessions.models import Session
from django.http import Http404
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, DetailView, ListView
import stripe
from decouple import config

stripe.api_key = config('STRIPE_API_KEY')

from .models import Booking

@login_required
def booking_view(request, booking_id):
    """View for a single booking."""
    try:
        booking = Booking.objects.get(id=booking_id)
    except Booking.DoesNotExist:
        raise render(request, 'atc_site/error.html', {'user': request.user, 'is_authenticated': request.user.is_authenticated, 'error': '404', 'title': 'Not Found', 'desc': 'The booking you are looking for does not exist.'})
    if request.user.is_superuser or booking.user == request.user:     
        return render(request, 'atc_site/booking/booking.html', {'user': request.user, 'is_authenticated': request.user.is_authenticated, 'booking': booking, 'invoice': stripe.Invoice.retrieve(booking.stripe_invoice_id), 'customer': stripe.Customer.retrieve(f'customuser-{booking.user.id}'), 'payment_intent': stripe.PaymentIntent.retrieve(booking.payment.stripe_payment_id)})
    return render(request, 'atc_site/error.html', {'user': request.user, 'is_authenticated': request.user.is_authenticated, 'error': '403', 'title': 'Access Forbidden', 'desc': 'You do not have permission to view this booking.'})