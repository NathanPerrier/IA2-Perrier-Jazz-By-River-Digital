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
from django.utils import timezone

stripe.api_key = config('STRIPE_API_KEY')
checkout_session = None

@csrf_exempt
@login_required
def create_ticket_checkout_session(request, event_id):
    global checkout_session
    # Assuming you have a function to get an event by ID
    event = Events.get_event(event_id)
    if event.available_tickets > 0:
        if event.sale_release_date < timezone.now() and event.sale_end_date > timezone.now():
            additional_items = []
            for item in EventFoodAndDrinks.objects.filter(event=event):
                additional_items.append(FoodAndDrinksItem.objects.get(id=item.food_and_drinks_item.id))
                
            for voucher in EventVoucher.objects.filter(event=event):    
                additional_items.append(voucher)

            try:
                checkout_session = stripe.checkout.Session.create(
                    customer=f'customuser-{str(request.user.id)}',
                    payment_method_types=['card'],
                    line_items=([   #! fix
                        {
                            'price': event.stripe_price_id,  
                            'quantity': 1,
                        }
                    ]) + ([{'price': str(item.stripe_price_id), 'quantity': 1, "adjustable_quantity": {"enabled": True, "minimum": 0, "maximum": get_stock(item)}} for item in additional_items]),
                    mode='payment',
                    success_url=request.build_absolute_uri(f'/events/{str(event.id)}/checkout/success/'),
                    cancel_url=request.build_absolute_uri(f'/events/{str(event.id)}/'),
                    customer_update={
                        'address': 'auto',
                    },
                    automatic_tax={'enabled': True},
                    billing_address_collection='required',
                    # cross_sell={'products': [[str(item.stripe_price_id) for item in food_and_drink_items]]} # [voucher.stripe_price_id for voucher in Voucher.objects.filter(id=[eventVoucher.id for eventVoucher in EventVoucher.objects.filter(event=event.id)])]]},
                )
                return redirect(checkout_session.url)
            except Exception as e:
                return JsonResponse({'error': str(e)})
        return render(request, 'atc_site//error.html', {'user': request.user, 'is_authenticated': request.user.is_authenticated, 'error' : '403', 'title' : 'Access Forbidden', 'desc' : 'This event is no longer available. Please contact the administrator if you believe this is an error.'})
    return render(request, 'atc_site//sold_out.html', {'user': request.user, 'is_authenticated': request.user.is_authenticated, 'event': event})
    
@login_required
def checkout_success(request, event_id):
    try:
        if stripe.checkout.Session.retrieve(checkout_session.id).payment_status == 'paid':
            invoice = stripe.Invoice.create(
                customer=checkout_session.customer,
                payment_method=request.POST.get('payment_method_id'),
                description=request.POST.get('description'),
                currency='aud',
                payment_intent=request.POST.get('payment_intent_id'),
                payment_settings={'payment_method_options': {'card': {'request_three_d_secure': 'automatic'}}},    
            )
            
            event = Events.get_event(event_id)
            event.available_tickets -= 1
            event.sold += 1
            event.save()
            
            BookingStatus.objects.create(
                status='Confirmed',
                user=request.user,
                payment_status=PaymentStatus.objects.get(status='PAID'),
                stripe_invoice_id=invoice.id,
            )
            
            Tickets.objects.create(
                user=request.user,
                event=event,
                sent=True,
                stripe_invoice_id=invoice.id,
            )

            Payment.objects.create(  #issue here
                user=request.user,
                amount=(checkout_session.amount_total/100),
                stripe_invoice_id=invoice.id,
                method=checkout_session.payment_method_types[0],
                currency=checkout_session.currency,
                stripe_payment_id=stripe.checkout.Session.retrieve(checkout_session.id).payment_intent,
                status=PaymentStatus.objects.get(status='PAID'),
            )
            
            Booking.objects.create(
                user=request.user,
                event=event,
                ticket=Tickets.objects.get(stripe_invoice_id=invoice.id),
                payment=Payment.objects.get(stripe_invoice_id=invoice.id),
                status=BookingStatus.objects.get(stripe_invoice_id=invoice.id),
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
                        code=Voucher.generate_code(),
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
                    
                    voucher.stripe_coupon_id = stripe_voucher.id
                    voucher.stripe_code_id = promo_code.id
                    voucher.code = make_password(voucher.code)
                    voucher.save()
            
                print('INVOICE')  
                stripe.InvoiceItem.create(
                    customer=checkout_session.customer,
                    quantity=product.quantity,
                    currency='aud',
                    price=product.price,
                    description=product.description,
                    invoice=invoice.id,
                )
            
            paid_invoice = stripe.Invoice.pay(invoice.id, paid_out_of_band=True)
            return redirect(paid_invoice.hosted_invoice_url, code=303)
        else:
            return redirect(f'/events/{str(event_id)}/checkout/', code=303)
    except Exception as e:
        return JsonResponse({'error': str(e)})

def get_stock(item):
    try:
        return item.stock
    except:
        return 1