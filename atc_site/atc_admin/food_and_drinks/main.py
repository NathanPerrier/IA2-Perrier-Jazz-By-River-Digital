from ..config import *

class FoodAndDrinksForm(forms.ModelForm):
    class Meta:
        model = FoodAndDrinks
        fields = '__all__'
    
    def clean_stock(self):
        quantity = self.cleaned_data.get('quantity')
        if quantity < 1:
            raise ValidationError('Quantity must be greater than 0')
        return quantity
    

    
class FoodAndDrinksAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    form = FoodAndDrinksForm
    list_display = ('item', 'quantity', 'user', 'event')
    search_fields = ('item', 'quantity', 'event')