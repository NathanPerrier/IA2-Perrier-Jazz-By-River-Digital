from django.db import models

class LocationImagesModel(models.Model):
    country = models.CharField(max_length=200, blank=False)
    city = models.TextField(blank=False)
    lat = models.FloatField()
    lon = models.FloatField()
    image_url = models.ImageField(upload_to='images/ai_images/')
    is_safe = models.BooleanField(default=False)
    