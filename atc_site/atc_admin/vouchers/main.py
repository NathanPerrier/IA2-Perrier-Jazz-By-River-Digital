from ..config import *
from django.utils import timezone
from atc_site.backend.atc.email import send_custom_emails

class VoucherForm(forms.ModelForm):
    class Meta:
        model = Voucher
        fields = '__all__'
        
    def clean_code(self):
        code = self.cleaned_data.get('code')
        if 'code' in self.changed_data and code and len(code) != 6:
            raise ValidationError('Reset code must be 6 characters long')
        return code

class VoucherAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    form = VoucherForm
    
    list_display = ('user', 'voucher', 'code', 'purchase_amount', 'amount_left', 'sent', 'expiration_date')
    search_fields = ('voucher', 'purchase_amount', 'amount_left', 'expiration_date')
    
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('<path:object_id>/delete/', self.admin_site.admin_view(self.delete_view), name='delete'),
        ]
        return custom_urls + urls
    
    def save_model(self, request, obj, form, change):
        print('code', obj.code)
        print('id', obj.id)
        try:
            voucher = stripe.Coupon.create(
                id=(f'voucher-{str(obj.id)}'),
                name=obj.voucher.name,
                amount_off=int(obj.purchase_amount*100),
                currency="aud",
                duration='forever',
                redeem_by=int(obj.expiration_date.timestamp()),
                applies_to={'products':[item.stripe_product_id for item in FoodAndDrinksItem.objects.filter(event=obj.event)]},
            )
            promo_code = stripe.PromotionCode.create(coupon=voucher.id, customer=(f'customuser-{obj.user.id}'), code=obj.code)
            
        except Exception as e:
            print(e)
            
            old_voucher = stripe.Coupon.retrieve(f'voucher-{str(obj.id)}')
            old_voucher.delete()
            old_code = stripe.PromotionCode.list(limit=1, coupon=old_voucher.id)
            
            voucher = stripe.Coupon.create(
                id=(f'voucher-{str(obj.id)}'),
                name=obj.voucher.name,
                amount_off=int(obj.amount_left*100),
                currency="aud",
                duration='forever',
                redeem_by=int(obj.expiration_date.timestamp()),
                applies_to={'products':[str(item.stripe_product_id) for item in FoodAndDrinksItem.objects.filter(event=obj.event)]},
            )
            
            promo_code = stripe.PromotionCode.create(coupon=voucher.id, customer=(f'customuser-{obj.user.id}'), code=(str(obj.code) if 'code' in form.changed_data else old_code['data'][0]['code']))
            
        if 'code' in form.changed_data:
            try:
                send_custom_emails(obj.user.email, obj.user.first_name, 'New Voucher Code', f'Your voucher code for {obj.event.name}, has been changed! This new voucher code can be used online or in-person. \nYour new voucher code is: \n \n {promo_code.code}')
                voucher.sent = True
            except Exception as e: 
                print(e)
                voucher.sent = False
            obj.code = make_password(obj.code)
   
        # link = stripe.PaymentLink.create(line_items=[{"price": price.id, "quantity": 1}])
        obj.stripe_code_id = promo_code.id
        obj.stripe_coupon_id = voucher.id  
        obj.save()   

        super().save_model(request, obj, form, change)
        
    
    def delete_view(self, request, object_id, extra_context=None):
        obj = self.get_object(request, object_id)
        
        try:
            stripe.Coupon.delete(f'voucher-{str(obj.id)}')
            stripe.PromotionCode.modify(id=obj.stripe_code_id, active=False)
        except Exception as e:
            print(e)
            
        obj.delete()
        return super().delete_view(request, object_id, extra_context)