from django.urls import path
from .views import *

urlpatterns = [
    path("chat/", chat, name="chat"),
    path("chat/change_model/", change_model, name="change_model"),
    path("chat/getCoordinates/", get_directions, name="get_directions"),
    path("chat/setRoute/", set_directions, name="set_directions"),
    path("chat/reset/", reset_messages, name="reset_messages")
]