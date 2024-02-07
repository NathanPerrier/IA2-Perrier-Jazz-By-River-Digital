from django.db import models
import hashlib

class UserLocationModel(models.Model):
    ip = models.CharField(max_length=256, blank=False)
    city = models.CharField(max_length=20, blank=False)
    region = models.CharField(max_length=20, blank=False)
    region_name = models.CharField(max_length=50, blank=False)
    country = models.CharField(max_length=100, blank=False)
    zip = models.CharField(max_length=10, blank=False)
    lat = models.CharField(max_length=20, blank=False)
    lon = models.CharField(max_length=20, blank=False)
    timezone = models.CharField(max_length=20, blank=False)
    country_code = models.CharField(max_length=10, blank=False)
    isp = models.CharField(max_length=100, blank=False)

    @staticmethod
    def hash_ip(ip):
        return hashlib.sha256(ip.encode()).hexdigest()
