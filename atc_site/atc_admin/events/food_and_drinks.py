from ..config import *


class FoodAndDrinksItemForm(forms.ModelForm):
    class Meta:
        model = FoodAndDrinksItem
        fields = '__all__'
    
    def clean_food_and_drinks_item(self):
        item = self.cleaned_data.get('food_and_drinks_item')
        if EventFoodAndDrinks.objects.filter(food_and_drinks_item=item).exists():
            raise ValidationError('Item already assigned to an event')
        return item
    
class EventFoodAndDrinksAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    form = FoodAndDrinksItemForm
    list_display = ('id', 'event', 'food_and_drinks_item')
    
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)