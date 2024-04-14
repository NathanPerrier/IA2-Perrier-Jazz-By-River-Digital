"""Models for the ``booking`` app."""
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import gettext_lazy as _

from django_countries.fields import CountryField

from ......models import CustomUser


class PaymentStatus(models.Model):
   status = models.CharField(max_length=256, blank=False)
   status_code = models.CharField(max_length=256, blank=False)
   last_modified = models.DateTimeField(auto_now=True, blank=False)
   creation_time = models.DateTimeField(auto_now_add=True, blank=False)
   
   def __str__(self):
      return self.status

class Payment(models.Model):
   user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
   amount = models.DecimalField(max_digits=10, decimal_places=2)
   currency = models.CharField(max_length=256, blank=False)
   stripe_invoice_id = models.CharField(max_length=256, blank=False)
   stripe_payment_id = models.CharField(max_length=256, blank=True, null=True)
   creation_time = models.DateTimeField(auto_now_add=True, blank=False)
   last_modified = models.DateTimeField(auto_now=True, blank=False)
   method = models.CharField(max_length=256, blank=False)
   status = models.ForeignKey(PaymentStatus, on_delete=models.CASCADE)