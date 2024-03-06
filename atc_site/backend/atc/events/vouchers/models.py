from django.db import models
from .....models import CustomUser
from ..models import Events

class Voucher(models.Model):
    code = models.CharField(max_length=255, unique=True)
    purchase_amount = models.DecimalField(max_digits=10, decimal_places=2)
    amount_left = models.DecimalField(max_digits=10, decimal_places=2)
    creation_time = models.DateTimeField(auto_now_add=True, blank=False)
    last_modified = models.DateTimeField(auto_now=True, blank=False)
    expiration_date = models.DateTimeField(blank=False)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.code
    
class EventVoucher(models.Model):
    voucher = models.ForeignKey(Voucher, on_delete=models.CASCADE)
    event = models.ForeignKey(Events, on_delete=models.CASCADE)