from django.db import models
from ..models import Events
from .....models import CustomUser
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError

    
class FoodAndDrinksItem(models.Model):
    name = models.CharField(max_length=200, blank=False)
    description = models.TextField(blank=False)
    price = models.DecimalField(max_digits=5, decimal_places=2, blank=False)
    stock = models.IntegerField(default=0, blank=False, validators=[MinValueValidator(0)]) #? min
    quantity_sold = models.IntegerField(default=0, blank=False, validators=[MinValueValidator(0)])
    creation_date = models.DateTimeField(auto_now_add=True, blank=False)
    last_modification = models.DateTimeField(auto_now=True, blank=False)
    vendor = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=False)

    
    def save(self, *args, **kwargs):
        if self.quantity_sold > self.stock:
            raise ValueError("Sold quantity cannot be more than available quantity")
        if self.vendor not in CustomUser.groups.filter(name='Vendor'):
            raise ValidationError("CustomUser must be in the Vendor group")
        super().save(*args, **kwargs)
    
class EventFoodAndDrinks(models.Model):
    event = models.ForeignKey(Events, on_delete=models.CASCADE)
    food_and_drinks_item = models.ForeignKey(FoodAndDrinksItem, on_delete=models.CASCADE)
    
    
class FoodAndDrinks(models.Model):
    item = models.ManyToManyField(FoodAndDrinksItem, blank=False)
    quantity = models.IntegerField(default=1, blank=False, validators=[MinValueValidator(1)])
    creation_date = models.DateTimeField(auto_now_add=True, blank=False)
    last_modification = models.DateTimeField(auto_now=True, blank=False)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True, null=True)
    event = models.ForeignKey(Events, on_delete=models.CASCADE)