from ..config import *

class FoodAndDrinksItemForm(forms.ModelForm):
    class Meta:
        model = FoodAndDrinksItem
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
    
class FoodAndDrinksItemAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    form = FoodAndDrinksItemForm
    list_display = ('name', 'description', 'price', 'stock', 'quantity_sold', 'vendor', 'image', 'last_modified')
    search_fields = ('name', 'price', 'description', 'stock', 'quantity_sold')
    
    def save_model(self, request, obj, form, change):
        try:
            product = stripe.Product.create(
                id=str(obj.id),
                name=obj.name,
                active=True,
                description=obj.description,
            )
            
            price = stripe.Price.create(
                product=product.id,
                unit_amount=int(obj.price*100),  
                currency="aud",
            )
            
            stripe.Product.modify(
                id=product.id,
                default_price=price.id,
            )
        except Exception as e:
            print(e)
            product = stripe.Product.modify(
                id=str(obj.id),
                name=obj.name,
                active=True,
                description=obj.description,
            )
            price = stripe.Price.create(
                product=product.id,
                unit_amount=int(obj.price*100),  
                currency="aud",
            )
            
            stripe.Product.modify(
                id=product.id,
                default_price=price.id,
            )
        # link = stripe.PaymentLink.create(line_items=[{"price": price.id, "quantity": 1}])
        obj.stripe_price_id = price.id
        super().save_model(request, obj, form, change)
        

        