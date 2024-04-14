from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_protect
import json

from .bot.main import ChatbotATC

from .models import Message


from .bot.__init__ import GPT_MODEL


@csrf_exempt
def reset_messages(request):
    # Delete MessageATCs for the current user
    Message.objects.filter(user=request.user).delete()

    # Create a system MessageATC
    try:
        Message.objects.create(role='system', content='You are a helpful chatbot designed to assist users and admins with certain site abilities such as editing their account, creationg or editing a booking, etc.', model=GPT_MODEL, user=request.user)
    except Exception as e:
        print('error:', e)
        
    return JsonResponse({'status': 'Messags reset successfully.'})


@require_POST
@csrf_exempt
def chat(request):
    print(request.user.first_name)

    user_message = request.POST.get('message')
    Message.objects.create(role='user', content=user_message, model=Message.objects.filter(user=request.user).all().order_by('timestamp').last().model, user=request.user)
    
    previous_MessageATCs = Message.objects.filter(user=request.user).all().order_by('timestamp')
    if previous_MessageATCs.count() > 0:
        
        formatted_messages = [{'role': msg.role, 'content': msg.content} for msg in previous_MessageATCs]
        
        # For Testing 
        print('###############################################################################################')
        print('formatted_messages:', formatted_messages)
        print('###############################################################################################')

        bot_response = ChatbotATC(previous_MessageATCs.last().model).chat_completion_request(formatted_messages)
        Message.objects.create(role='assistant', content=bot_response, model=previous_MessageATCs.last().model, user=request.user)
    else:
        bot_response = ChatbotATC(GPT_MODEL).chat_completion_request(request.POST.get('MessageATC'))
        Message.objects.create(role='assistant', content=bot_response, model=GPT_MODEL, user=request.user)
    print(Message.objects.all())
    return JsonResponse({'message': bot_response})

@require_POST
@csrf_exempt
def change_model(request):
    Message.objects.create(role='system', content=f'You are now using the {request.POST.get("model")} model', model=request.POST.get('model'), user=request.user)
    return JsonResponse({'success': True})

