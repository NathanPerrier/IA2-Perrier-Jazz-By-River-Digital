from ..config import *
from urllib.parse import quote_from_bytes

class EventsForm(forms.ModelForm):
    class Meta:
        model = Events
        fields = '__all__'
    
    

class EventsAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    form = EventsForm
    list_display = ('name', 'description', 'location', 'date', 'time', 'available_tickets', 'sold', 'organizer', 'ticket_price', 'sale_release_date', 'sale_end_date', 'image' ,'last_modified')
    search_fields = ('name', 'description', 'location', 'date', 'time', 'available_tickets', 'sold', 'sale_release_date', 'sale_end_date', 'organizer', 'ticket_price', 'image')

    def save_model(self, request, obj, form, change):
        try:
            product = stripe.Product.create(
                id=f'events-{str(obj.id)}',
                name=obj.name,
                active=True,
                description=obj.description,
                url=request.build_absolute_uri(f'/events/{str(obj.id)}/'),
            )
            
            price = stripe.Price.create(
                product=product.id,
                unit_amount=int(obj.ticket_price*100),  
                currency="aud",
            )
            
            stripe.Product.modify(
                id=product.id,
                default_price=price.id,
            )
        except Exception as e:
            print(e)
            product = stripe.Product.modify(
                id=f'events-{str(obj.id)}',
                name=obj.name,
                active=True,
                description=obj.description,
                url=request.build_absolute_uri(f'/events/{str(obj.id)}/'),
            )
            price = stripe.Price.create(
                product=product.id,
                unit_amount=int(obj.ticket_price*100),  
                currency="aud",
            )
            
            stripe.Product.modify(
                id=product.id,
                default_price=price.id,
            )
        # link = stripe.PaymentLink.create(line_items=[{"price": price.id, "quantity": 1}])
        obj.stripe_price_id = price.id
        super().save_model(request, obj, form, change)
