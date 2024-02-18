import os
from django.http import StreamingHttpResponse, JsonResponse
from django.conf import settings
from .models import Newsletter
from .main import *

from django.contrib.auth import logout
from .email import send_contact_emails, send_newsletter_emails

def logout_view(request):
    logout(request)
    return index(request)

def register_view(request):
    return register_page(request)
    
def forgot_password_view(request):
    return forgot_password_page(request)

def stream_video_atc_site(request, video_path):
    video_path = os.path.join(settings.BASE_DIR, 'atc_site\\frontend\\static\\atc_site\\videos', video_path)
    def play_video(video_path):
        with open(video_path, 'rb') as video:
            for chunk in iter(lambda: video.read(4096), b""):
                yield chunk

    response = StreamingHttpResponse(play_video(video_path))
    response['Content-Type'] = 'video/mp4'
    return response


def contact_ajax(request):
    print("contact_ajax")
    if request.method == 'POST':
        print(request.POST['name'])
        send_contact_emails(request.POST['email'], settings.EMAIL_HOST_USER, request.POST['name'], request.POST['subject'], request.POST['message'])
        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False})
    
def newsletter_ajax(request):
    if request.method == 'POST':
        email = request.POST['email']
        if Newsletter.objects.filter(email=email).exists():
            return JsonResponse({'success': False})
        else:
            send_newsletter_emails(email, settings.EMAIL_HOST_USER)
            Newsletter.objects.create(email=email)
            return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False})