"""Models for the ``booking`` app."""
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import gettext_lazy as _

from .tickets.models import Tickets
from ...events.models import Events
from .payment.models import Payment
from .....models import CustomUser
from ..vouchers.models import Voucher
from ..food_and_drinks.models import FoodAndDrinks

class BookingStatus(models.Model):
   pass


class Booking(models.Model):
   user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
   event = models.ForeignKey(Events, on_delete=models.CASCADE)
   tickets = models.ForeignKey(Tickets, on_delete=models.CASCADE)
   payment = models.ForeignKey(Payment, on_delete=models.CASCADE)
   status = models.ForeignKey(BookingStatus, on_delete=models.CASCADE)
   vouchers = models.ManyToManyField(Voucher, blank=True)
   food_and_drinks = models.ManyToManyField(FoodAndDrinks, blank=True)
   creation_time = models.DateTimeField(auto_now_add=True, blank=False)
   last_modified = models.DateTimeField(auto_now=True, blank=False)