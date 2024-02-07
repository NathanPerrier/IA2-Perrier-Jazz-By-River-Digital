from django.db import models
from atc_site.models import CustomUser, CustomUserManager
import hashlib

class Message(models.Model):
    role = models.CharField(max_length=200)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    model = models.CharField(max_length=50, blank=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)


class Route(models.Model):
    ip = models.CharField(max_length=200, blank=False)
    route = models.CharField(max_length=200)
    start = models.CharField(max_length=200)
    end = models.CharField(max_length=200)
    mode = models.CharField(max_length=200)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    @staticmethod
    def hash_ip(ip):
        return hashlib.sha256(ip.encode()).hexdigest()