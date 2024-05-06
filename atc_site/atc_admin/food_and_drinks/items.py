from ..config import *

class FoodAndDrinksItemForm(forms.ModelForm):
    """
    A form class for creating and updating instances of the FoodAndDrinksItem model.

    Attributes:
        model (FoodAndDrinksItem): The model associated with the form.
        fields (list or tuple): The fields to include in the form.

    Methods:
        clean_quantity: Validates the quantity field to ensure it is greater than 0.
        clean_vendor: Validates the vendor field to ensure it belongs to the Vendor group.
    """
    
    class Meta:
        model = FoodAndDrinksItem
        fields = '__all__'
    
    def clean_quantity(self):
        # get the quantity field from the form
        quantity = self.cleaned_data.get('quantity') 
        
        # check if the quantity is less than 1
        if quantity < 1:
            raise ValidationError('Quantity must be greater than 0')
        return quantity
    
    def clean_vendor(self):
        # get the vendor field from the form
        vendor = self.cleaned_data.get('vendor')
        
        # get the Vendor group
        vendor_group = Group.objects.get(name='Vendor')
        
        # check if the vendor is not in the Vendor group
        if vendor not in CustomUser.objects.filter(groups=vendor_group):
            raise ValidationError("CustomUser must be in the Vendor group")
        return vendor
    
class FoodAndDrinksItemAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    """
    A form class for creating and updating instances of the FoodAndDrinksItem model.

    Attributes:
        model (FoodAndDrinksItem): The model associated with the form.
        fields (list or tuple): The fields to include in the form.

    Methods:
        clean_quantity: Validates the quantity field to ensure it is greater than 0.
        clean_vendor: Validates the vendor field to ensure it belongs to the Vendor group.
    """
    
    # set the form to the FoodAndDrinksItemForm class
    form = FoodAndDrinksItemForm
    list_display = ('name', 'description', 'price', 'stock', 'quantity_sold', 'vendor', 'image', 'last_modified')
    search_fields = ('name', 'price', 'description', 'stock', 'quantity_sold')
    
    def get_urls(self):
        """ This method overrides the get_urls method of the parent class and adds a custom URL pattern for deleting an object. """
        urls = super().get_urls()
        custom_urls = [
            path('<path:object_id>/delete/', self.admin_site.admin_view(self.delete_view), name='delete'),
        ]
        return custom_urls + urls
    
    def save_model(self, request, obj, form, change):
        try:
            product = stripe.Product.create(
                id=f'food-and-drinks-{str(obj.id)}',
                name=obj.name.capitalize(),
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
            
            for voucher in Voucher.objects.filter(event=obj.event):
                stripe.Coupon.modify(
                    id=f'voucher-{str(voucher.id)}',
                    applies_to={'products':[f'food-and-drinks-{item.id}' for item in FoodAndDrinksItem.objects.filter(event=obj.event)]},
                )
                
        except Exception as e:
            print(e)
            product = stripe.Product.modify(
                id=f'food-and-drinks-{str(obj.id)}',
                name=obj.name.capitalize(),
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
        obj.stripe_product_id = product.id
        obj.save()
        super().save_model(request, obj, form, change)
        

    
    def delete_view(self, request, object_id, extra_context=None):
        obj = self.get_object(request, object_id)
        
        try:
            stripe.Product.delete(id=f'food-and-drinks-{str(obj.id)}')
            stripe.Price.modify(id=obj.stripe_price_id, active=False)
        except Exception as e:
            print(e)
            
        obj.delete()
        return super().delete_view(request, object_id, extra_context)