import os
from django.http import StreamingHttpResponse, JsonResponse
from django.conf import settings
from .models import Newsletter
import stripe
from decouple import config
from django.contrib.auth.decorators import login_required
from .main import *

stripe.api_key = config('STRIPE_API_KEY')

from django.contrib.auth import logout
from .email import send_contact_emails, send_newsletter_emails

def logout_view(request):
    logout(request)
    return index(request)

def register_view(request):
    return register_page(request)
    
def forgot_password_view(request):
    return forgot_password_page(request)

@login_required
def billing_portal_view(request):
    configuration = stripe.billing_portal.Configuration.create(
        features={
            'customer_update': {
            'allowed_updates': ['tax_id', 'address', 'phone'],
            'enabled': True,
            },
            'invoice_history': {
            'enabled': True,
            },
            'payment_method_update': {
            'enabled': True,
            },
        },
        business_profile={
            'privacy_policy_url': 'http://localhost:8000/terms%20and%20policies/privacy%20policy',
            'terms_of_service_url': 'http://localhost:8000/terms%20and%20policies/terms%20and%20conditions',
        },
    )
    billing_portal = stripe.billing_portal.Session.create(
        customer=f'customuser-{str(request.user.id)}',
        return_url="http://localhost:8000/",
        configuration=configuration.id,
    )
   
    return redirect(billing_portal.url)

@login_required
def stripe_dashboard(request):
    account = stripe.Account.create_login_link(f'customuser-{str(request.user.id)}')
    return redirect(account.url, code=303)

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