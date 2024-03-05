from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import gettext_lazy as _

from ....events.models import Events

class Tickets(models.Model):
   event = models.ForeignKey(Events, on_delete=models.CASCADE)
   creation_date = models.DateTimeField(auto_now_add=True, blank=False)
   sent = models.BooleanField(default=False)