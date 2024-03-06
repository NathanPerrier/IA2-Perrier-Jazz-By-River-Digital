from django.db import models
from ..models import Events
from .....models import CustomUser
    
class FoodAndDrinksItem(models.Model):
    name = models.CharField(max_length=200, blank=False)
    description = models.TextField(blank=False)
    price = models.DecimalField(max_digits=5, decimal_places=2, blank=False)
    stock = models.IntegerField(default=0, blank=False) #? min
    quantity_sold = models.IntegerField(default=0, blank=False) #? min
    discount = models.FloatField(blank=True) #? min
    creation_date = models.DateTimeField(auto_now_add=True, blank=False)
    last_modification = models.DateTimeField(auto_now=True, blank=False)
    vendor = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=False)
    
class EventFoodAndDrinks(models.Model):
    event = models.ForeignKey(Events, on_delete=models.CASCADE)
    food_and_drinks_item = models.ForeignKey(FoodAndDrinksItem, on_delete=models.CASCADE)
    
    
class FoodAndDrinks(models.Model):
    item = models.ManyToManyField(FoodAndDrinksItem, blank=False)
    quantity = models.IntegerField(default=0, blank=False)
    creation_date = models.DateTimeField(auto_now_add=True, blank=False)
    last_modification = models.DateTimeField(auto_now=True, blank=False)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True, null=True)
    event = models.ForeignKey(Events, on_delete=models.CASCADE)