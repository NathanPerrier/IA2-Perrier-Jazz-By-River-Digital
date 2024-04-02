from ..config import *

class EventFoodAndDrinksAdmin(admin.ModelAdmin):
    list_display = ('id', 'event', 'food_and_drinks_item')