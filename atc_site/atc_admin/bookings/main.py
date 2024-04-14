from typing import Any
from ..config import *

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = '__all__'
    
class BookingAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('user', 'event', 'ticket', 'payment', 'last_modified')
    search_fields = ('event', 'status')
    
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('<path:object_id>/delete/', self.admin_site.admin_view(self.delete_view), name='delete'),
        ]
        return custom_urls + urls
    
    def save_model(self, request: Any, obj: Any, form: Any, change: Any):
        
        try:
            invoice = stripe.Invoice.modify(
                id=obj.stripe_invoice_id,
                customer=f'customuser-{obj.user.id}',
                collection_method='send_invoice',
                days_until_due=7,
                description=f'Booking for {obj.event.name} on {obj.event.date} at {obj.event.time}',
                metadata={
                    'booking_id': obj.id,
                    'event_id': obj.event.id,
                    'ticket_id': obj.ticket.id,
                    'user_id': obj.user.id,
                }
            )  
        except Exception as e:
            print(e)
            invoice = stripe.Invoice.create(
                customer=f'customuser-{obj.user.id}',
                collection_method='send_invoice',
                days_until_due=7,
                description=f'Booking for {obj.event.name} on {obj.event.date} at {obj.event.time}',
                metadata={
                    'booking_id': obj.id,
                    'event_id': obj.event.id,
                    'ticket_id': obj.ticket.id,
                    'user_id': obj.user.id,
                }
            )
            
            
        obj.stripe_invoice_id = invoice.id
        obj.payment.stripe_invoice_id = invoice.id
        obj.ticket.stripe_invoice_id = invoice.id
        obj.status.stripe_invoice_id = invoice.id
        
        obj.save()
        obj.ticket.save()
        obj.payment.save()
        obj.status.save()
        return super().save_model(request, obj, form, change)
    
    def delete_view(self, request, object_id, extra_context=None):
        print('deleting booking ')
        obj = self.get_object(request, object_id)
        try:
            refund = stripe.Refund.create(
                payment_intent=obj.payment.stripe_payment_id,
                #amount=int(obj.payment.amount*100),
            )
            # stripe.PaymentIntent.cancel(obj.payment.stripe_payment_id)
            stripe.Invoice.modify(id=obj.stripe_invoice_id, payment_intent=refund.payment_intent)
            
            print(' delete stripe items')
            
            food_and_drink_items = BookingFoodAndDrinks.objects.filter(booking=obj)
            for item in food_and_drink_items:
                item.food_and_drinks.item.stock += item.food_and_drinks.quantity
                item.food_and_drinks.item.quantity_sold -= item.food_and_drinks.quantity
                item.food_and_drinks.item.save()
            
            BookingFoodAndDrinks.objects.filter(booking=obj).delete() #? obj.id?
            BookingVouchers.objects.filter(booking=obj).delete()
            
            Tickets.objects.get(stripe_invoice_id=obj.stripe_invoice_id).delete()
            Payment.objects.get(stripe_invoice_id=obj.stripe_invoice_id).delete()
            BookingStatus.objects.get(stripe_invoice_id=obj.stripe_invoice_id).delete()
            
        except Exception as e:
            print(e)
            
        event = obj.event
        event.available_tickets += 1
        event.sold -= 1
        
        event.save()
        
        return super().delete_view(request, object_id, extra_context)