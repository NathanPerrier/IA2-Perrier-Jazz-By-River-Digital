from django.db import models
from django.contrib.auth.hashers import make_password, check_password
from django.core.validators import EmailValidator
from django.utils import timezone
from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from atc_site.models import CustomUser, CustomUserManager
import random
import string

class ForgotPasswordAuth(models.Model):
    '''Model to store the signup code and its expiration time'''
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    reset_code = models.CharField(max_length=256, blank=False)
    expiration_time = models.DateTimeField(blank=False)
    creation_time = models.DateTimeField(auto_now_add=True, blank=False)
    
    @classmethod
    def create_entry(cls, user, reset_code, expiration_time):
        return ForgotPasswordAuth(user=user, reset_code=reset_code, expiration_time=expiration_time)

    @classmethod
    def check_email(cls, email):
        try:
            return CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            return None
        
    @classmethod
    def get_by_user_id(cls, user):
        try:
            return ForgotPasswordAuth.objects.get(user=user)
        except CustomUser.DoesNotExist:
            return None
        
    @classmethod
    def delete_by_user_id(cls, user):
        user = cls.get_by_user_id(user)  
        if user:
            user.delete()
            
    def if_user_is_verified(self, email):
        try:
            user = ForgotPasswordAuth.objects.get(email=email)
            return user.verified
        except ForgotPasswordAuth.DoesNotExist:
            return False

    @staticmethod
    def generate_code(length=6):
        return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))

    @classmethod
    def store_code(cls, email, code, expiration_duration=1800):
        user = cls.check_email(email)
        if user:
            expiration_time = timezone.now() + timezone.timedelta(seconds=expiration_duration)
            reset_entry = cls.create_entry(user=user, reset_code=make_password(code), expiration_time=expiration_time)
            reset_entry.save()

    @classmethod
    def create_and_send_reset_code(cls, email):
        if cls.check_email(email):
            if cls.check_active_code(email):
                code = cls.generate_code()
                cls.store_code(email, code)
                cls.send_code(code, cls.check_email(email))
                return True, None
            return True, None
        return False, "Invalid Email"

    @classmethod
    def check_active_code(cls, email):
        return not ForgotPasswordAuth.objects.filter(user=cls.check_email(email), expiration_time__gt=timezone.now()).exists()

    @staticmethod
    def check_code(code, user_code):
        return check_password(user_code, code)

    @classmethod
    def check_code_entry(cls, email, input_code):
        reset_entry = ForgotPasswordAuth.objects.filter(user=cls.check_email(email)).order_by('-creation_time').first()
        if not reset_entry:
            print('no reset entry')
            return False, "No reset code found for the user"

        if not cls.check_code(reset_entry.reset_code, input_code):
            print('invalid reset code')
            return False, "Invalid reset code"

        if timezone.now() > reset_entry.expiration_time:
            print('reset code expired')
            return False, "Reset code has expired"

        print('reset code valid')
        return True, None

    @classmethod
    def send_code(cls, code, user):
        # Send email to the admin
        context = {
            'name': 'New User',
            'email': user.email,
            'subject': 'Your Password Reset Code',
            'message': f'Hi {user.first_name}, here is your registration code:\n\n {code}',
        }
        email_body = render_to_string('email.html', context)

        email = EmailMessage(
            'RainCheck - Registration Code',
            email_body,
            settings.EMAIL_HOST_USER,
            [user.email]
        )
        email.content_subtype = 'html'
        email.fail_silently = False
        email.send()
        
