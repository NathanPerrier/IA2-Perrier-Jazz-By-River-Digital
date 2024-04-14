from ..config import *

class BookingFoodAndDrinksForm(forms.ModelForm):
    class Meta:
        model = FoodAndDrinks
        fields = '__all__'
    
class BookingFoodAndDrinksAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('food_and_drinks', 'user', 'booking')
    
    