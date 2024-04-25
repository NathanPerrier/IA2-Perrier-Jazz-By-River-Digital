import stripe
from decouple import config
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password

from .food_and_drinks.models import FoodAndDrinks, FoodAndDrinksItem, EventFoodAndDrinks, BookingFoodAndDrinks
from .vouchers.models import Voucher, EventVoucher, BookingVouchers
from .booking.models import Booking, BookingStatus
from .booking.tickets.models import Tickets
from .booking.payment.models import Payment, PaymentStatus
from .models import Events
from ..email import send_custom_emails
from django.utils import timezone


stripe.api_key = config('STRIPE_API_KEY')
checkout_session = None

@csrf_exempt
@login_required
def create_ticket_checkout_session(request, event_id):
    global checkout_session
  
    event = Events.get_event(event_id)
    allowed_groups = event.target_groups.all()
    if event.available_tickets > 0:
        if event.sale_release_date < timezone.now() and event.sale_end_date > timezone.now():
            if request.user.is_superuser or request.user == event.organizer or (event.target_groups and request.user.groups.filter(id__in=allowed_groups).exists()) or event.target_groups.count() == 0:
                additional_items = []
                
                for item in EventFoodAndDrinks.objects.filter(event=event):
                    additional_items.append(FoodAndDrinksItem.objects.get(id=item.food_and_drinks_item.id))
                    
                for voucher in EventVoucher.objects.filter(event=event):    
                    additional_items.append(voucher)

                try:
                    items=[]
                    for item in additional_items:
                        if check_stock(item): items.append({'price': str(item.stripe_price_id), 'quantity': 1, "adjustable_quantity": {"enabled": True, "minimum": 0, "maximum": get_stock(item)}})
                        
                    checkout_session = stripe.checkout.Session.create(
                        customer=f'customuser-{str(request.user.id)}',
                        payment_method_types=['card'],
                        line_items=([  
                            {
                                'price': event.stripe_price_id,  
                                'quantity': 1,
                            }
                        ]) + items,
                        mode='payment',
                        success_url=request.build_absolute_uri(f'/events/{str(event.id)}/checkout/success/'),
                        cancel_url=request.build_absolute_uri(f'/events/{str(event.id)}/'),
                        customer_update={
                            'address': 'auto',
                        },
                        automatic_tax={'enabled': True},
                        allow_promotion_codes=True,
                        billing_address_collection='required',
                    )
                    return redirect(checkout_session.url)
                except Exception as e: return render(request, 'atc_site//error.html', {'user': request.user, 'is_authenticated': request.user.is_authenticated, 'error' : '500', 'title' : 'Internal Server Error', 'desc' : f'{e}. Please try again later.'})
            return render(request, 'atc_site//error.html', {'user': request.user, 'is_authenticated': request.user.is_authenticated, 'error' : '403', 'title' : 'Access Forbidden', 'desc' : 'You do not have permission to access this event.'})
        return render(request, 'atc_site//error.html', {'user': request.user, 'is_authenticated': request.user.is_authenticated, 'error' : '403', 'title' : 'Access Forbidden', 'desc' : 'This event is no longer available. Please contact the administrator if you believe this is an error.'})
    return render(request, 'atc_site//sold_out.html', {'user': request.user, 'is_authenticated': request.user.is_authenticated, 'event': event})
    
def checkout_success(request, event_id):
    try:
        if stripe.checkout.Session.retrieve(checkout_session.id).payment_status == 'paid':
            invoice = stripe.Invoice.create(
                customer=checkout_session.customer,
                payment_method=request.POST.get('payment_method_id'),
                description=request.POST.get('description'),
                currency='aud',
                payment_intent=checkout_session.payment_intent,
                payment_settings={'payment_method_options': {'card': {'request_three_d_secure': 'automatic'}}},    
            )

            event = Events.get_event(event_id)
            event.available_tickets -= 1
            event.sold += 1
            event.save()
            
            booking_status = BookingStatus.objects.create(
                status='Confirmed',
                user=request.user,
                payment_status=PaymentStatus.objects.get(status='PAID'),
                stripe_invoice_id=invoice.id,
            )
            
            ticket = Tickets.objects.create(
                user=request.user,
                event=event,
                sent=True,
                stripe_invoice_id=invoice.id,
            )
            
            payment = Payment.objects.create(  #issue here
                user=request.user,
                amount=(invoice.total/100),
                stripe_invoice_id=invoice.id,
                method=checkout_session.payment_method_types[0],
                currency=checkout_session.currency,
                stripe_payment_id=stripe.checkout.Session.retrieve(checkout_session.id).payment_intent,
                status=PaymentStatus.objects.get(status='PAID'),
            )

            
            booking = Booking.objects.create(
                user=request.user,
                event=event,
                ticket=ticket,
                payment=payment,
                status=booking_status,
                stripe_invoice_id=invoice.id,
            )
            
            food_and_drinks = []
            vouchers= []
            
            for product in checkout_session.list_line_items():
                print('FOOD AND DRINKS')
                if product.price.id in [item.stripe_price_id for item in FoodAndDrinksItem.objects.all()]:
                    print('FOOD AND DRINKS ITEM')
                    print(product.price.id)
                    food_and_drink = FoodAndDrinks.objects.create(
                        user=request.user,
                        event=event,
                        quantity=product.quantity,
                        item=EventFoodAndDrinks.objects.get(food_and_drinks_item=FoodAndDrinksItem.objects.get(stripe_price_id=product.price.id)),
                    )
                    
                    BookingFoodAndDrinks.objects.create(
                        food_and_drinks=food_and_drink,
                        user=request.user,
                        booking=Booking.objects.get(stripe_invoice_id=invoice.id),
                    )
                    
                    print('FOOD AND DRINKS ITEM CREATED')
                    item = FoodAndDrinksItem.objects.get(stripe_price_id=product.price.id)
                    item.stock -= product.quantity
                    item.quantity_sold += product.quantity
                    item.save()
                    
                if product.price.id in [item.stripe_price_id for item in EventVoucher.objects.all()]:
                    print('VOUCHER')
                    event_voucher=EventVoucher.objects.get(stripe_price_id=product.price.id)
                    
                    voucher = Voucher.objects.create(
                        user=request.user,
                        voucher=event_voucher,
                        code=Voucher.generate_code().capitalize(),
                        purchase_amount=product.price.unit_amount/100,
                        amount_left=product.price.unit_amount/100,
                        event=event,
                        expiration_date=timezone.now() + timezone.timedelta(days=365),
                    )
                    
                    stripe_voucher = stripe.Coupon.create(
                        id=f'voucher-{str(voucher.id)}',
                        name=event_voucher.name,
                        amount_off=product.price.unit_amount,
                        currency="aud",
                        duration='forever',
                        redeem_by=timezone.now() + timezone.timedelta(days=365),
                        applies_to={'products':[item.stripe_product_id for item in FoodAndDrinksItem.objects.filter(event=event)]},
                    )
                    promo_code = stripe.PromotionCode.create(coupon=stripe_voucher.id, customer=checkout_session.customer, code=voucher.code)
                    
                    BookingVouchers.objects.create(
                        voucher=voucher,
                        user=request.user,
                        booking=Booking.objects.get(stripe_invoice_id=invoice.id),
                    )
                    
                    #remove??
                    send_custom_emails(request.user.email, request.user.first_name, 'Voucher Purchased', f'Thank you for purchasing a voucher for {event.name}, this voucher can be used online or in-person. \nYour code is: \n \n {voucher.code}')
                    
                    voucher.stripe_coupon_id = stripe_voucher.id
                    voucher.stripe_code_id = promo_code.id
                    voucher.code = make_password(voucher.code)
                    voucher.save()
                    
                if (stripe.checkout.Session.retrieve(checkout_session.id).total_details.amount_discount > 0 and product.description != event.name):
                    product_price = stripe.Price.create(
                        product=product.price.product,
                        unit_amount=0,
                        currency='aud',
                    )
                
                    stripe.InvoiceItem.create(
                        # id=f'invoice-{booking.id}',
                        customer=checkout_session.customer,
                        quantity=product.quantity,
                        currency='aud',
                        price=product_price.id,
                        description=product.description,
                        invoice=invoice.id,
                    )
                else:
                    stripe.InvoiceItem.create(
                        # id=f'invoice-{booking.id}',
                        customer=checkout_session.customer,
                        quantity=product.quantity,
                        currency='aud',
                        price=product.price.id,
                        description=product.description,
                        invoice=invoice.id,
                    )
            
                    
            if stripe.checkout.Session.retrieve(checkout_session.id).total_details.amount_discount > 0:
                session = stripe.checkout.Session.retrieve(checkout_session.id, expand=['total_details.breakdown'])
                stripe_voucher = session.total_details.breakdown.discounts[0].discount.coupon.id
                voucher = Voucher.objects.get(stripe_coupon_id=stripe_voucher)
                
                amount_left = float(voucher.amount_left) - session.total_details.amount_discount/100
                
                stripe_voucher = stripe.Coupon.retrieve(voucher.stripe_coupon_id).delete()
                promo_code = stripe.PromotionCode.retrieve(voucher.stripe_code_id)
                
                stripe_voucher = stripe.Coupon.create(
                    id=f'voucher-{str(voucher.id)}',
                    name=voucher.voucher.name,
                    amount_off=int(amount_left*100),
                    currency="aud",
                    duration='forever',
                    redeem_by=timezone.now() + timezone.timedelta(days=365),
                    applies_to={'products':[item.stripe_product_id for item in FoodAndDrinksItem.objects.filter(event=event)]},
                )
                promo_code = stripe.PromotionCode.create(coupon=stripe_voucher.id, customer=session.customer, code=promo_code.code)

                voucher.amount_left = amount_left
                voucher.stripe_code_id = promo_code.id
                voucher.stripe_coupon_id = stripe_voucher.id
                voucher.save()

               
            paid_invoice = stripe.Invoice.pay(invoice.id, paid_out_of_band=True)
            
            payment.amount = paid_invoice.total/100
            payment.save()
            
            return redirect(paid_invoice.hosted_invoice_url, code=303)
        else: return redirect(f'/events/{str(event_id)}/checkout/', code=303)
    except Exception as e: return render(request, 'atc_site//error.html', {'user': request.user, 'is_authenticated': request.user.is_authenticated, 'error' : '500', 'title' : 'Internal Server Error', 'desc' : f'{e}. Please try again later.'})

def get_stock(item):
    try:
        return item.stock
    except:
        return 1
    
def check_stock(item):
    try:
        if item.stock > 0: return True
        return False
    except:
        return True