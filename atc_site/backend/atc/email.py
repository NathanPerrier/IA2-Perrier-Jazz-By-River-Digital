from django.core.mail import send_mail
from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

def send_contact_emails(user_email, admin_email, name, subject, message):
    context = {
        'name': name,
        'email': user_email,
        'subject': 'New contact message',
        'message': f'''subject: {subject} 
        messgae: {message}''',
    }
    email_body = render_to_string('atc_site/email.html', context)

    email = EmailMessage(
        'New contact message',
        email_body,
        settings.EMAIL_HOST_USER,
        [admin_email]
    )
    email.content_subtype = 'html'
    email.fail_silently = False
    email.send()

    context = {
        'name': name,
        'email': user_email,
        'subject': 'Thank you for contacting us!',
        'message': f'Thanks {name} for sending us a message. We will get back to you as soon as possible.',
    }
    email_body = render_to_string('atc_site/email.html', context)

    email = EmailMessage(
        'Thank you for contacting us',
        email_body,
        settings.EMAIL_HOST_USER,
        [user_email]
    )
    email.content_subtype = 'html'
    email.fail_silently = False
    email.send()

    
def send_newsletter_emails(user_email, admin_email):
    # Send email to the admin
    context = {
        'name': 'New User',
        'email': user_email,
        'subject': 'New Subscriber',
        'message': f'{user_email} has just subscribed to the newsletter',
    }
    email_body = render_to_string('atc_site/email.html', context)

    email = EmailMessage(
        'Thank you for contacting us',
        email_body,
        settings.EMAIL_HOST_USER,
        [user_email]
    )
    email.content_subtype = 'html'
    email.fail_silently = False
    email.send()
    
    context = {
        'name': 'New User',
        'email': user_email,
        'subject': 'Thank you for subscribing!',
        'message': f'Thanks {user_email} for subscribing to our newsletter. You will now recieve our weekly newsletter.',
    }
    email_body = render_to_string('atc_site/email.html', context)

    email = EmailMessage(
        'Thank you for subscribing',
        email_body,
        settings.EMAIL_HOST_USER,
        [user_email]
    )
    email.content_subtype = 'html'
    email.fail_silently = False
    email.send()
