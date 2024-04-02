from ..config import *

class FoodAndDrinksForm(forms.ModelForm):
    class Meta:
        model = FoodAndDrinks
        fields = '__all__'
    
    def clean_quantity(self):
        quantity = self.cleaned_data.get('quantity')
        if quantity < 1:
            raise ValidationError('Quantity must be greater than 0')
        return quantity
    
    def clean_vendor(self):
        vendor = self.cleaned_data.get('vendor')
        vendor_group = Group.objects.get(name='Vendor')
        if vendor not in CustomUser.objects.filter(groups=vendor_group):
            raise ValidationError("CustomUser must be in the Vendor group")
        return vendor
    
class FoodAndDrinksItemAdmin(admin.ModelAdmin):
    form = FoodAndDrinksForm
    list_display = ('name', 'price', 'description')
    search_fields = ('name', 'price', 'description')

        