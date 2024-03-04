"""Views for the booking app."""
from django.contrib.auth.decorators import login_required
from django.contrib.sessions.models import Session
from django.http import Http404
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, DetailView, ListView

from .models import Booking

