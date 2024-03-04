"""Models for the ``booking`` app."""
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import gettext_lazy as _

from django_countries.fields import CountryField

from ....models import CustomUser

class Event(models.Model):
   name = models.CharField(max_length=256, blank=False)
   description = models.TextField(blank=False)
   location = models.CharField(max_length=256, blank=False)
   available_tickets = models.IntegerField(blank=False)
   sold = models.IntegerField(blank=False)
   sale_release_date = models.DateTimeField(blank=False)
   sale_end_date = models.DateTimeField(blank=False)
   creation_time = models.DateTimeField(auto_now_add=True, blank=False)
   last_modified = models.DateTimeField(auto_now=True, blank=False)
   organizer = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
   ticket_price = models.DecimalField(max_digits=10, decimal_places=2)
   currency = CountryField()
   
   