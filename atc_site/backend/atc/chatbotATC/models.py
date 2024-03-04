from django.db import models
from atc_site.models import CustomUser, CustomUserManager
import hashlib

class MessageATC(models.Model):
    role = models.CharField(max_length=200)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    model = models.CharField(max_length=50, blank=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)

