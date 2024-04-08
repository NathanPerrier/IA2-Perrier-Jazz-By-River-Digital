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