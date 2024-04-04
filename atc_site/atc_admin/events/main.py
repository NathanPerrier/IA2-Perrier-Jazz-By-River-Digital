from ..config import *


class EventsForm(forms.ModelForm):
    class Meta:
        model = Events
        fields = '__all__'
    
    

class EventsAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    form = EventsForm
    list_display = ('name', 'description', 'location', 'date', 'time', 'available_tickets', 'sold', 'organizer', 'ticket_price', 'sale_release_date', 'sale_end_date', 'image' ,'last_modified')
    search_fields = ('name', 'description', 'location', 'date', 'time', 'available_tickets', 'sold', 'sale_release_date', 'sale_end_date', 'organizer', 'ticket_price', 'image')

    def save_model(self, request, obj, form, change):
        if change: #! doesn't work
            pass
            # product = stripe.Product.modify(
            #     id=obj.id,
            #     name=obj.name,
            #     active=True,
            #     description=obj.description,
            #     images=[obj.image.url],
            #     # default_price=price.id,
            # )
            # price = stripe.Price.modify(
            #     product=obj.id,
            #     unit_amount=obj.ticket_price*100,  
            #     currency="AUD",
            # )
            
            # stripe.Product.modify(
            #     id=product.id,
            #     default_price=price.id,
            # )
            
            # link = stripe.PaymentLink.modify(line_items=[{"price": price.id, "quantity": 1}])
            # obj.payment_link = link.url
            
        else:
            product = stripe.Product.create(
                id=obj.id,
                name=obj.name,
                active=True,
                description=obj.description,
                # images=[obj.image.url],  #! fix this
            )
            
            price = stripe.Price.create(
                product=product.id,
                unit_amount=obj.ticket_price*100,  
                currency="AUD",
            )
            
            stripe.Product.modify(
                id=product.id,
                default_price=price.id,
            )
            
            link = stripe.PaymentLink.create(line_items=[{"price": price.id, "quantity": 1}])
            obj.payment_link = link.url
        super().save_model(request, obj, form, change)
