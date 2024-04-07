import stripe
from decouple import config
from django.http import JsonResponse
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .food_and_drinks.models import FoodAndDrinks, FoodAndDrinksItem, EventFoodAndDrinks
from .vouchers.models import Voucher, EventVoucher
from .models import Events

stripe.api_key = config('STRIPE_API_KEY')
checkout_session = None

@csrf_exempt
@login_required
def create_ticket_checkout_session(request, event_id):
    global checkout_session
    # Assuming you have a function to get an event by ID
    event = Events.get_event(event_id)
    food_and_drink_items = [FoodAndDrinksItem.objects.filter(id=eventItem.id).all() for eventItem in EventFoodAndDrinks.objects.filter(event=event.id).all()]
    food_and_drink_items = [item for queryset in food_and_drink_items for item in queryset]
    print(food_and_drink_items)
    try:
        checkout_session = stripe.checkout.Session.create(
            customer=f'customuser-{str(request.user.id)}',
            payment_method_types=['card'],
            line_items=([
                {
                    'price': event.stripe_price_id,  
                    'quantity': 1,
                }
            ]) + ([{'price': str(item.stripe_price_id), 'quantity': 1, "adjustable_quantity": {"enabled": True, "minimum": 0, "maximum": item.stock}} for item in food_and_drink_items]),
            mode='payment',
            success_url=request.build_absolute_uri(f'/events/{str(event.id)}/checkout/success/'),
            cancel_url=request.build_absolute_uri(f'/events/{str(event.id)}/'),
            customer_update={
                'address': 'auto',
            },
            automatic_tax={'enabled': True},
            # cross_sell={'products': [[str(item.stripe_price_id) for item in food_and_drink_items]]} # [voucher.stripe_price_id for voucher in Voucher.objects.filter(id=[eventVoucher.id for eventVoucher in EventVoucher.objects.filter(event=event.id)])]]},
        )
        return redirect(checkout_session.url)
    except Exception as e:
        return JsonResponse({'error': str(e)})
    
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
            for product in checkout_session.list_line_items():
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
