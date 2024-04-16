from django.db import models
from .....models import CustomUser
from ..booking.models import Booking
from ..models import Events

import random, string   
from django.contrib.auth.hashers import make_password, check_password 
    
class EventVoucher(models.Model):
    name = models.CharField(max_length=200, blank=False)
    description = models.TextField(blank=False)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    event = models.ForeignKey(Events, on_delete=models.CASCADE)
    stripe_price_id = models.CharField(max_length=256, blank=True, null=True)
    
class Voucher(models.Model):
    voucher = models.ForeignKey(EventVoucher, on_delete=models.CASCADE)
    code = models.CharField(max_length=512, unique=True)
    purchase_amount = models.DecimalField(max_digits=10, decimal_places=2)
    amount_left = models.DecimalField(max_digits=10, decimal_places=2)
    creation_time = models.DateTimeField(auto_now_add=True, blank=False)
    last_modified = models.DateTimeField(auto_now=True, blank=False)
    expiration_date = models.DateTimeField(blank=False)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True, null=True)
    event = models.ForeignKey(Events, on_delete=models.CASCADE)
    stripe_coupon_id = models.CharField(max_length=256, blank=True, null=True)
    stripe_code_id = models.CharField(max_length=256, blank=True, null=True)

      
      
    @staticmethod
    def generate_code(length=6):
        return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))

  
    @staticmethod
    def check_code(code, user_code):
        return check_password(user_code, code)

    
class BookingVouchers(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    voucher = models.ForeignKey(Voucher, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    
        
    