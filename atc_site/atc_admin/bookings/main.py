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
            payment_intent = stripe.PaymentIntent.create(
                amount=int(obj.ticket.price*100),
                currency="aud",
                payment_method_types=["card"],
                customer=obj.user.stripe_customer_id,
                description=f'Booking for {obj.event.name} on {obj.event.date} at {obj.event.time}',
                receipt_email=obj.user.email,
                metadata={
                    'booking_id': obj.id,
                    'event_id': obj.event.id,
                    'ticket_id': obj.ticket.id,
                    'user_id': obj.user.id,
                }
            )
            
            invoice = stripe.Invoice.modify(
                id=f'invoice-{str(obj.id)}',
                customer=obj.user.stripe_customer_id,
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
            
            stripe.PaymentIntent.confirm(payment_intent.id)  
        except Exception as e:
            print(e)
            payment_intent = stripe.PaymentIntent.create(
                amount=int(obj.payment.amount*100),
                currency="aud",
                payment_method_types=["card"],
                customer=obj.user.stripe_customer_id,
                description=f'Booking for {obj.event.name} on {obj.event.date} at {obj.event.time}',
                receipt_email=obj.user.email,
                metadata={
                    'booking_id': obj.id,
                    'event_id': obj.event.id,
                    'ticket_id': obj.ticket.id,
                    'user_id': obj.user.id,
                }
            )
            
            invoice = stripe.Invoice.create(
                id=f'invoice-{str(obj.id)}',
                customer=obj.user.stripe_customer_id,
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
            
            stripe.PaymentIntent.confirm(payment_intent.id)
            
        obj.stripe_invoice_id = invoice.id
        obj.payment.stripe_payment_id = payment_intent.id
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
        
        stripe.PaymentIntent.cancel(obj.payment.stripe_payment_id)
        stripe.Invoice.delete(obj.payment.stripe_invoice_id)
        
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
        
        event = obj.event
        event.available_tickets += 1
        event.sold -= 1
        
        event.save()
        
        return super().delete_view(request, object_id, extra_context)