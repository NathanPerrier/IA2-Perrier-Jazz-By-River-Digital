import stripe
from decouple import config
from django.http import JsonResponse
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from .food_and_drinks.models import FoodAndDrinks, FoodAndDrinksItem, EventFoodAndDrinks
from .vouchers.models import Voucher, EventVoucher
from .models import Events

@csrf_exempt
def create_ticket_checkout_session(request, event_id):
    # Assuming you have a function to get an event by ID
    event = Events.get_event(event_id)
    stripe.api_key = config('STRIPE_API_KEY')
    food_and_drink_items = [FoodAndDrinksItem.objects.filter(id=eventItem.id).all() for eventItem in EventFoodAndDrinks.objects.filter(event=event.id)]
    food_and_drink_items = [item for queryset in food_and_drink_items for item in queryset]
    try:
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price': event.stripe_price_id,  
                'quantity': 1,
            }],
            mode='payment',
            success_url=request.build_absolute_uri(f'/events/{str(event.id)}/checkout/success/'),
            cancel_url=request.build_absolute_uri(f'/events/{str(event.id)}/'),
            automatic_tax={'enabled': True},
            # invoice_creation={'enabled': True},
            # cross_sell={'products': [[str(item.stripe_price_id) for item in food_and_drink_items]]} # [voucher.stripe_price_id for voucher in Voucher.objects.filter(id=[eventVoucher.id for eventVoucher in EventVoucher.objects.filter(event=event.id)])]]},
        )
        return redirect(checkout_session.url)
    except Exception as e:
        return JsonResponse({'error': str(e)})
    
    # return redirect(checkout_session.url, code=303)
