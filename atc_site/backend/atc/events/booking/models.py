"""Models for the ``booking`` app."""
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import gettext_lazy as _

from .tickets.models import Tickets
from ...events.models import Events
from .payment.models import Payment, PaymentStatus
from .....models import CustomUser
from ..vouchers.models import Voucher
from ..food_and_drinks.models import FoodAndDrinks

class BookingStatus(models.Model):
   status = models.CharField(max_length=50, blank=False)
   user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
   payment_status = models.ForeignKey(PaymentStatus, on_delete=models.CASCADE)
   last_modified = models.DateTimeField(auto_now=True, blank=False)
   stripe_invoice_id = models.CharField(max_length=256, blank=True, null=True)

class Booking(models.Model):
   user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
   event = models.ForeignKey(Events, on_delete=models.CASCADE)
   ticket = models.ForeignKey(Tickets, on_delete=models.CASCADE)
   payment = models.ForeignKey(Payment, on_delete=models.CASCADE)
   status = models.ForeignKey(BookingStatus, on_delete=models.CASCADE)
   vouchers = models.ManyToManyField(Voucher, blank=True)
   food_and_drinks = models.ManyToManyField(FoodAndDrinks, blank=True)
   stripe_invoice_id = models.CharField(max_length=256, blank=True, null=True)
   creation_time = models.DateTimeField(auto_now_add=True, blank=False)
   last_modified = models.DateTimeField(auto_now=True, blank=False)
   
   @classmethod
   def get_booking(cls, booking_id):
      return cls.objects.get(pk=booking_id)
   
   @classmethod
   def get_bookings(cls):
      return cls.objects.all()
   
   @classmethod
   def get_bookings_by_user(cls, user_id):
      return cls.objects.filter(user=user_id)
   
   @classmethod
   def get_bookings_by_event(cls, event_id):
      return cls.objects.filter(event=event_id)
   
   @classmethod
   def get_bookings_by_status(cls, status_id):
      return cls.objects.filter(status=status_id)