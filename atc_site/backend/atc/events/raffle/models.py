# from django.db import models
# from .....models import CustomUser
# from ..models import Events    
    
# class EventRaffle(models.Model):
#     name = models.CharField(max_length=200, blank=False)
#     description = models.TextField(blank=False)
        # offer fields
#     event = models.ForeignKey(Events, on_delete=models.CASCADE)
    
# class Raffle(models.Model):
#     raffle = models.ForeignKey(EventRaffle, on_delete=models.CASCADE)
#     code = models.CharField(max_length=255, unique=True)
#     purchase_amount = models.DecimalField(max_digits=10, decimal_places=2)
#     creation_time = models.DateTimeField(auto_now_add=True, blank=False)
#     last_modified = models.DateTimeField(auto_now=True, blank=False)
#     expiration_date = models.DateTimeField(blank=False)
#     user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True, null=True)

#     def __str__(self):
#         return self.code