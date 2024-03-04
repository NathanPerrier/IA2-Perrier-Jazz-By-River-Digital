"""Models for the ``booking`` app."""
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import gettext_lazy as _

from .tickets.models import Tickets
from ...events.models import Event
from .payment.models import Payment
from .....models import CustomUser

from django_countries.fields import CountryField



class BookingStatus(models.Model):
   pass


class Booking(models.Model):
   user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
   event = models.ForeignKey(Event, on_delete=models.CASCADE)
   tickets = models.ForeignKey(Tickets, on_delete=models.CASCADE)
   payment = models.ForeignKey(Payment, on_delete=models.CASCADE)
   status = models.ForeignKey(BookingStatus, on_delete=models.CASCADE)
   creation_time = models.DateTimeField(auto_now_add=True, blank=False)
   last_modified = models.DateTimeField(auto_now=True, blank=False)