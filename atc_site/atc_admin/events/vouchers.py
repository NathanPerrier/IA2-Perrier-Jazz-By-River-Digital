from ..config import *

class EventVoucherAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('name', 'description', 'event', 'stripe_price_id')
    search_fields = ('name', 'description')
    
    def save_model(self, request, obj, form, change):
        try:
            product = stripe.Product.create(
                id=f'event-voucher-{str(obj.id)}',
                name=obj.name,
                description=obj.description,
                active=True,
            )
            
            price = stripe.Price.create(
                product=product.id,
                unit_amount=5000,
                currency="aud",
            )
            
            stripe.Product.modify(
                id=product.id,
                default_price=price.id,
            )
            
                
        except Exception as e:
            print(e)
            product = stripe.Product.modify(
                id=f'event-voucher-{str(obj.id)}',
                name=obj.name,
                active=True,
                description=obj.description,
            )
            price = stripe.Price.create(
                product=product.id,
                unit_amount=5000,
                currency="aud",
            )
            
            stripe.Product.modify(
                id=product.id,
                default_price=price.id,
            )
        # link = stripe.PaymentLink.create(line_items=[{"price": price.id, "quantity": 1}])
        obj.stripe_price_id = price.id
        print(obj.stripe_price_id)
        super().save_model(request, obj, form, change)