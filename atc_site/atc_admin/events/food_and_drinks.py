from ..config import *

class EventFoodAndDrinksAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('id', 'event', 'food_and_drinks_item')