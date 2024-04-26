from ..config import *
from urllib.parse import quote_from_bytes
from django.utils import timezone

class EventsForm(forms.ModelForm):
    class Meta:
        model = Events
        fields = '__all__'
        
    def clean_image(self):
        image = self.cleaned_data.get('image')
        if not image:
            raise ValidationError('Image is required')
        return image

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if not name:
            raise ValidationError('Name is required')
        return name
    
    def clean_description(self):
        description = self.cleaned_data.get('description')
        if not description:
            raise ValidationError('Description is required')
        return description
    
    def clean_location(self):
        location = self.cleaned_data.get('location')
        if not location:
            raise ValidationError('Location is required')
        return location

    def clean_date(self):
        date = self.cleaned_data.get('date')
        if not date:
            raise ValidationError('Date is required')
        
        if date < timezone.now():
            raise ValidationError('Date cannot be in the past')
        return date
    
    def clean_time(self):
        time = self.cleaned_data.get('time')
        if not time:
            raise ValidationError('Time is required')
        return time
    
    def clean_available_tickets(self):
        available_tickets = self.cleaned_data.get('available_tickets')
        if not available_tickets:
            raise ValidationError('Available tickets is required')
        if available_tickets < 0:
            raise ValidationError('Available tickets cannot be negative')
        return available_tickets
    
    def clean_sold(self):
        sold = self.cleaned_data.get('sold')
        if not sold and sold != 0:
            raise ValidationError('Sold is required')
        if sold < 0:
            raise ValidationError('Sold cannot be negative')
        return sold
    
    def clean_organizer(self):
        organizer = self.cleaned_data.get('organizer')
        if not organizer:
            raise ValidationError('Organizer is required')
        admin_group = Group.objects.get(name='Admin')
        organizer_group = Group.objects.get(name='Organizer')
        if organizer not in CustomUser.objects.filter(groups=admin_group) or organizer not in CustomUser.objects.filter(groups=organizer_group):
            raise ValidationError('Organizer must be an admin or organizer')
        return organizer
    
    def clean_ticket_price(self):
        ticket_price = self.cleaned_data.get('ticket_price')
        if not ticket_price and (int(ticket_price) != 0):
            raise ValidationError('Ticket price is required')
        if ticket_price < 0:
            raise ValidationError('Ticket price cannot be negative')
        return ticket_price
    
    def clean_sale_release_date(self):
        sale_release_date = self.cleaned_data.get('sale_release_date')
        if not sale_release_date:
            raise ValidationError('Sale release date is required')
        if self.cleaned_data.get('sale_end_date'):
            if sale_release_date > self.cleaned_data.get('sale_end_date'):
                raise ValidationError('Sale end date cannot be before the sale release date')
        if self.cleaned_data.get('date'):
            if sale_release_date > self.cleaned_data.get('date'):
                raise ValidationError('Sale release date cannot be after the event date')
        return sale_release_date
    
    def clean_sale_end_date(self):
        sale_end_date = self.cleaned_data.get('sale_end_date')
        if not sale_end_date:
            raise ValidationError('Sale end date is required')
        if self.cleaned_data.get('sale_release_date'):
            if sale_end_date < self.cleaned_data.get('sale_release_date'):
                raise ValidationError('Sale end date cannot be before the sale release date')
        return sale_end_date
    
    def clean_target_groups(self):
        target_groups = self.cleaned_data.get('target_groups')
        print(target_groups)
        for group in target_groups:
            if group not in Group.objects.all():
                raise ValidationError('Target groups must be a valid group')
        return target_groups

    

class EventsAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    form = EventsForm
    list_display = ('name', 'description', 'location', 'date', 'time', 'available_tickets', 'sold', 'organizer', 'ticket_price', 'sale_release_date', 'sale_end_date', 'image' ,'last_modified')
    search_fields = ('name', 'description', 'location', 'date', 'time', 'available_tickets', 'sold', 'sale_release_date', 'sale_end_date', 'organizer', 'ticket_price', 'image')

    
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('<path:object_id>/delete/', self.admin_site.admin_view(self.delete_view), name='delete'),
        ]
        return custom_urls + urls

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
        obj.save()
        super().save_model(request, obj, form, change)

    def delete_view(self, request, object_id, extra_context=None):
        obj = self.get_object(request, object_id)
        
        try:
            stripe.Product.delete(f'events-{str(obj.id)}')
            stripe.Price.modify(id=obj.stripe_price_id, active=False)
        except Exception as e:
            print(e)
            
        obj.delete()        
        return super().delete_view(request, object_id, extra_context)