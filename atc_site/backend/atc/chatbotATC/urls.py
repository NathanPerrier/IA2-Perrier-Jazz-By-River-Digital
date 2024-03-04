from django.urls import path
from .views import *

urlpatterns = [
    path("chat/", chat, name="chat"),
    path("chat/change_model/", change_model, name="change_model"),
    
    #** OTHER stuff like admin, booking and account functionality goes here
    
    path("chat/reset/", reset_messages, name="reset_messages")
]