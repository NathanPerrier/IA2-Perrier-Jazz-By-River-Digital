from django.db import models

class FoodAndDrinks(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    quantity = models.IntegerField(default=0)
    creation_date = models.DateTimeField(auto_now_add=True, blank=False)
    last_modification = models.DateTimeField(auto_now=True, blank=False)