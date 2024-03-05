"""Models for the ``booking`` app."""
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import gettext_lazy as _

from django_countries.fields import CountryField



from ....models import CustomUser

class Events(models.Model):
   name = models.CharField(max_length=256, blank=False)
   description = models.TextField(blank=False)
   location = models.CharField(max_length=256, blank=False)
   date = models.DateTimeField(blank=False)
   time = models.TimeField(blank=False)
   available_tickets = models.IntegerField(blank=False)
   sold = models.IntegerField(blank=False)
   sale_release_date = models.DateTimeField(blank=False)
   sale_end_date = models.DateTimeField(blank=False)
   creation_time = models.DateTimeField(auto_now_add=True, blank=False)
   last_modified = models.DateTimeField(auto_now=True, blank=False)
   organizer = models.ForeignKey(CustomUser, on_delete=models.CASCADE)  #* whoever creates the event
   ticket_price = models.DecimalField(max_digits=10, decimal_places=2)
   vouchers = models.ManyToManyField('Voucher', blank=True)
   food_and_drinks = models.ManyToManyField('FoodAndDrinks', blank=True)
   schedule = models.ForeignKey('EventSchedule', on_delete=models.CASCADE, blank=True, null=True)
   image = models.ImageField(upload_to='images/events/', blank=True, null=True)
   
class EventSchedule(models.Model):
   event = models.ForeignKey(Events, on_delete=models.CASCADE)
   event_item = models.ManyToManyField('EventScheduleItem')
   
class EventScheduleItem(models.Model):
   start_time = models.TimeField(blank=False)
   end_time = models.TimeField(blank=False)
   title = models.CharField(max_length=256, blank=False)
   description = models.TextField(blank=False)
   creation_time = models.DateTimeField(auto_now_add=True, blank=False)
   last_modified = models.DateTimeField(auto_now=True, blank=False)
   
