from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_protect
import json

from .bot.main import Chatbot

from .models import Message, Route

from .bot.data import BotData

from .bot.__init__ import GPT_MODEL
from ..location.main import GetLocation


@csrf_exempt
def reset_messages(request):
    # Delete messages for the current user
    Message.objects.filter(user=request.user).delete()

    # Create a system message
    try:
        Message.objects.create(role='system', content='You are a helpful weather assistant that has access to almost all weather data. You are to answer purely weather-based questions. Try to include figures in your response to justify your reasoning.', model=GPT_MODEL, user=request.user)
    except Exception as e:
        print('error:', e)
        
    return JsonResponse({'status': 'Messages reset successfully.'})


@require_POST
@csrf_exempt
def chat(request):
    print(request.user.first_name)
    user_message = request.POST.get('message')
    Message.objects.create(role='user', content=user_message, model=Message.objects.filter(user=request.user).all().order_by('timestamp').last().model, user=request.user)
    
    previous_messages = Message.objects.filter(user=request.user).all().order_by('timestamp')
    if previous_messages.count() > 0:
        
        formatted_messages = [{'role': msg.role, 'content': msg.content} for msg in previous_messages]
        
        # For Testing 
        print('###############################################################################################')
        print('formatted_messages:', formatted_messages)
        print('###############################################################################################')

        bot_response = Chatbot(previous_messages.last().model).chat_completion_request(formatted_messages)
        Message.objects.create(role='assistant', content=bot_response, model=previous_messages.last().model, user=request.user)
    else:
        bot_response = Chatbot(GPT_MODEL).chat_completion_request(request.POST.get('message'))
        Message.objects.create(role='assistant', content=bot_response, model=GPT_MODEL, user=request.user)
    print(Message.objects.all())
    return JsonResponse({'message': bot_response})

@require_POST
@csrf_exempt
def change_model(request):
    Message.objects.create(role='system', content=f'You are now using the {request.POST.get("model")} model', model=request.POST.get('model'), user=request.user)
    return JsonResponse({'success': True})

@csrf_protect
@require_POST
def get_directions(request):
    if request.method == 'POST':
        route = Route.objects.filter(ip=Route.hash_ip(GetLocation().get_ip_address())).last() if Route.objects.filter(ip=Route.hash_ip(GetLocation().get_ip_address())).exists() else Route()
        data = json.loads(request.body)
        bot = BotData().WeatherRoute()
        bot.routeStart, route.start = data['start'], data['start']
        bot.routeEnd, route.end = data['end'], data['end']
        bot.routeMode, route.mode = data['mode'], data['mode']
        route.route = list(bot.get_route())
        route.ip = Route.hash_ip(GetLocation().get_ip_address())
        route.save()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})

def set_directions(request):
    if Route.objects.filter(ip=Route.hash_ip(GetLocation().get_ip_address())).exists():
        route = Route.objects.filter(ip=Route.hash_ip(GetLocation().get_ip_address())).last()
        return JsonResponse({'success': True, 'route': route.route, 'mode': route.mode})
    return JsonResponse({'success': False})