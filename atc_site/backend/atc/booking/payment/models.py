"""Models for the ``booking`` app."""
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import gettext_lazy as _

from django_countries.fields import CountryField

from .....models import CustomUser


class PaymentStatus(models.Model):
   status = models.CharField(max_length=256, blank=False)
   # payment status message
   status_message = models.CharField(max_length=256, blank=False)
   # payment status time
   status_time = models.DateTimeField(auto_now=True, blank=False)
   # payment status raw
   status_raw = models.TextField(blank=False)
   # payment status code
   status_code = models.CharField(max_length=256, blank=False)
   # payment status message
   status_message = models.CharField(max_length=256, blank=False)
   # payment status time
   status_time = models.DateTimeField(auto_now=True, blank=False)
   # payment status raw
   status_raw = models.TextField(blank=False)
   # payment status code
   status_code = models.CharField(max_length=256, blank=False)
   # payment status message
   status_message = models.CharField(max_length=256, blank=False)
   # payment status time
   status_time = models.DateTimeField(auto_now=True, blank=False)



class Payment(models.Model):
   user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
   amount = models.DecimalField(max_digits=10, decimal_places=2)
   currency = CountryField()
   status = models.ForeignKey(PaymentStatus, on_delete=models.CASCADE)
   creation_time = models.DateTimeField(auto_now_add=True, blank=False)
   last_modified = models.DateTimeField(auto_now=True, blank=False)
   # payment gateway specific fields
   gateway = models.CharField(max_length=256, blank=False)
   gateway_transaction_id = models.CharField(max_length=256, blank=False)
   gateway_response = models.TextField(blank=False)
   gateway_response_code = models.CharField(max_length=256, blank=False)
   gateway_response_message = models.CharField(max_length=256, blank=False)
   gateway_response_time = models.DateTimeField(auto_now=True, blank=False)
   gateway_response_raw = models.TextField(blank=False)
   # payment method specific fields
   method = models.CharField(max_length=256, blank=False)
   method_transaction_id = models.CharField(max_length=256, blank=False)
   method_response = models.TextField(blank=False)
   method_response_code = models.CharField(max_length=256, blank=False)
   method_response_message = models.CharField(max_length=256, blank=False)
   method_response_time = models.DateTimeField(auto_now=True, blank=False)
   method_response_raw = models.TextField(blank=False)
   # payment details
   payment_details = models.TextField(blank=False)
   # payment status
   status = models.ForeignKey(PaymentStatus, on_delete=models.CASCADE)