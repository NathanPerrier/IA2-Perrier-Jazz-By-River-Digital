from django.contrib import admin
from django.urls import include, path
from .views import stream_video_atc_site, contact_ajax, newsletter_ajax
from . import main

urlpatterns = [
    path("", main.index, name="atc_index"),
    path("erea", main.erea, name="erea"),
    
    path("subjects", main.subjects, name="subjects"),
    path("subjects/english", main.english, name="english"),
    path("subjects/maths", main.maths, name="maths"),
    path("subjects/music", main.music, name="music"),
    path("subjects/religion", main.religion, name="religion"),
    path("subjects/science", main.science, name="science"),
    path("subjects/technology", main.technology, name="technology"),
    
    path("terms and policies", main.terms, name="terms and policies"),
    path("terms and policies/terms of use", main.terms_of_use, name="terms of use"),
    path("terms and policies/cookie policy", main.cookie, name="cookie policy"),
    path("terms and policies/safety policy", main.safety, name="safety policy"),
    path("terms and policies/copyright policy", main.copyright, name="copyright"),
    path("terms and policies/terms and conditions", main.terms_conditions, name="terms and conditions"),
    path("terms and policies/privacy policy", main.privacy, name="privacy policy"),
    
    path('contact_ajax/', contact_ajax, name='contact_ajax'),
    path('newsletter_ajax/', newsletter_ajax, name='newsletter_ajax'),
    path('stream_video/<str:video_path>/', stream_video_atc_site, name='stream_video_atc_site'),
]