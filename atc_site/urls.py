"""
URL configuration for atc_site project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static

from django.contrib.auth import views as auth_views
from django.contrib import admin
from django.urls import include, path

from .backend import main, views
from .backend.views import stream_video, get_user_location
from .backend.chatbot.views import chat

urlpatterns = [
    path("", include("atc_site.backend.atc.urls"), name="atc_site"),

    path("", include("atc_site.backend.chatbot.urls"), name="chatbot"),

    # path("", main.index, name="index"),
    # path("radar", main.radar, name="radar"),
    # path("routes", main.routes, name="routes"),
    # path("search", main.search, name="search"),
    # path("search/<str:location>", views.search_location, name="search_location"),
    # path("saved", main.saved, name="saved"),
    # path("search/", main.search, name="search"),
    
    path('login', views.loginView, name='login'),
    
    path('register/', views.register_view, name='register'),
    path('register/get_email/', views.register_get_email_view, name='register_get_email'),
    path('register/get_code/', views.register_get_code_view, name='register_get_code'),
    path('register/set_password/', views.register_set_password_view, name='register_set_password'),
    
    path('forgot/', views.forgot_password_view, name='forgot_password'),
    path('forgot/get_email/', views.forgot_password_get_email_view, name='forgot_password_get_email'),
    path('forgot/get_code/', views.forgot_password_get_code_view, name='forgot_password_get_code'),
    path('forgot/set_password/', views.forgot_password_set_password_view, name='forgot_password_set_password'),
    
    path('logout/', views.logout_view, name='logout'),
    
    path("admin", admin.site.urls),
    
    path('stream_video/<str:video_path>/', stream_video, name='stream_video'),
    path('get_user_location/', get_user_location, name='get_user_location'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if not settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)