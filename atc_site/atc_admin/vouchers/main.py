from ..config import *
from django.utils import timezone

class VoucherForm(forms.ModelForm):
    class Meta:
        model = Voucher
        fields = '__all__'
        
    def clean_code(self):
        cleaned_data = super().clean()
        code = cleaned_data.get('code')
        if 'code' in self.changed_data and code and len(code) != 6:
            raise ValidationError('Reset code must be 6 characters long')
        return cleaned_data


class VoucherAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    form = VoucherForm
    
    list_display = ('user', 'voucher', 'code', 'purchase_amount', 'amount_left', 'expiration_date')
    search_fields = ('voucher', 'purchase_amount', 'amount_left', 'expiration_date')
    
    def save_model(self, request, obj, form, change):
        try:
            voucher = stripe.Coupon.create(
                id=f'voucher-{str(obj.id)}',
                name=obj.voucher.name,
                amount_off=int(obj.purchase_amount*100),
                currency="aud",
                duration='forever',
                redeem_by=int(obj.expiration_date.timestamp()),
                applies_to={'products':[item.stripe_product_id for item in FoodAndDrinksItem.objects.filter(event=obj.event)]},
            )
            promo_code = stripe.PromotionCode.create(coupon=voucher.id, customer=f'customuser-{request.user.id}', code=obj.code)
            
        except Exception as e:
            print(e)
            voucher = stripe.Coupon.modify(
                id=f'voucher-{str(obj.id)}',
                name=obj.voucher.name,
                amount_off=int(obj.purchase_amount*100),
                currency="aud",
                duration='forever',
                redeem_by=int(obj.expiration_date.timestamp()),
                applies_to={'products':[item.stripe_product_id for item in FoodAndDrinksItem.objects.filter(event=obj.event)]},
            )
            promo_code = stripe.PromotionCode.modify(coupon=voucher.id, customer=f'customuser-{request.user.id}', code=obj.code)
        
        if 'code' in form.changed_data:
            obj.code = make_password(obj.code)
   
        # link = stripe.PaymentLink.create(line_items=[{"price": price.id, "quantity": 1}])
        obj.stripe_code_id = promo_code.id
        obj.stripe_coupon_id = voucher.id     
        super().save_model(request, obj, form, change)