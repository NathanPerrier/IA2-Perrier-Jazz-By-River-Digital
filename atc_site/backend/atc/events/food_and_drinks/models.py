from django.db import models
from ..models import Events
from .....models import CustomUser
    
class FoodAndDrinksItem(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    discount = models.FloatField(blank=True)
    event = models.ForeignKey(Events, on_delete=models.CASCADE)
    
class FoodAndDrinks(models.Model):
    item = models.ManyToManyField(FoodAndDrinksItem, blank=False)
    quantity = models.IntegerField(default=0)
    creation_date = models.DateTimeField(auto_now_add=True, blank=False)
    last_modification = models.DateTimeField(auto_now=True, blank=False)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True, null=True)
    event = models.ForeignKey(Events, on_delete=models.CASCADE)