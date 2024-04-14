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
    
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('<path:object_id>/delete/', self.admin_site.admin_view(self.delete_view), name='delete'),
        ]
        return custom_urls + urls
    
    def save_model(self, request, obj, form, change):
        try:
            product = stripe.Product.create(
                id=f'food-and-drinks-{str(obj.id)}',
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
            
            for voucher in Voucher.objects.filter(event=obj.event):
                stripe.Coupon.modify(
                    id=f'voucher-{str(voucher.id)}',
                    applies_to={'products':[f'food-and-drinks-{item.id}' for item in FoodAndDrinksItem.objects.filter(event=obj.event)]},
                )
                
        except Exception as e:
            print(e)
            product = stripe.Product.modify(
                id=f'food-and-drinks-{str(obj.id)}',
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
        obj.stripe_product_id = product.id
        super().save_model(request, obj, form, change)
        

    
    def delete_view(self, request, object_id, extra_context=None):
        obj = self.get_object(request, object_id)
        
        stripe.Product.delete(id=f'food-and-drinks-{str(obj.id)}')
        stripe.Price.modify(id=obj.stripe_price_id, active=False)
        
        return super().delete_view(request, object_id, extra_context)