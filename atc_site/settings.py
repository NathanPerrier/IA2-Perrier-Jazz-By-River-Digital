# from django.urls import reverse_lazy
# from two_factor.urls import urlpatterns as tf_urls
# from django_otp.admin import OTPAdminSite
# from two_factor.views import LoginView
# import django_two_factor_auth
from pathlib import Path
import socket
import os

env_path = '.env'

from decouple import config, Csv

# Build paths inside the project like this: BASE_DIR / 'subdir'
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

SECRET_KEY = config('SECRET_KEY')

PORT = '8000'

DEBUG = True

CSRF_TRUSTED_ORIGIN = [
    "https://host.docker.internal:8000/",
    "https://host.docker.internal:8000",
    "host.docker.internal",
    "localhost",
    'https://*.host.docker.internal:8000',
    'https://*.127.0.0.1',
    'https://stunning-carnival-5jvx655grg4h457v-8000.preview.app.github.dev'
]

ALLOWED_HOSTS = [socket.gethostbyname(socket.gethostname()), '192.168.68.71', 'https://stunning-carnival-5jvx655grg4h457v-8000.preview.app.github.dev', '127.0.0.1', 'localhost', 'app-ia1-weather-app-django-1-dev-ok-z1qk8tbu.livecycle.run', 'host.docker.internal', 'ouguiya-wooden.runblade.host', '192.168.68.67', '192.168.0.178', '192.168.68.64', '192.168.68.62']

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'django_otp',
    'django_otp.plugins.otp_static',
    'django_otp.plugins.otp_totp',
    'two_factor',
    'corsheaders',
    "django_browser_reload",
    # "axes",
    
    "atc_site",
    "atc_site.backend.weather_app",
    "atc_site.backend.weather_app.locationImage",
    "atc_site.backend.location",
    "atc_site.backend.atc.chatbotATC",
    "atc_site.backend.weather_app.chatbot",
    "atc_site.backend.atc",
    "atc_site.backend.atc.events",
    "atc_site.backend.atc.events.booking",
    "atc_site.backend",
    "atc_site.backend.auth.forgot_password",
    "atc_site.unitTests",
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    'django_otp.middleware.OTPMiddleware',  # Required for django_two_factor_auth
    "allauth.account.middleware.AccountMiddleware",
    # "axes.middleware.AxesMiddleware",
]

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
    # 'axes.backends.AxesBackend',
    # 'axes.backends.AxesStandaloneBackend',  
)

ROOT_URLCONF = "atc_site.urls"

default_app_config = 'atc_site.apps.ATC_SiteConfig'

# CORS_ALLOW_ALL_ORIGINS = True

# # Or, if you want to allow specific origins
# CORS_ALLOWED_ORIGINS = [
#     "http://host.docker.internal:8000",
# ]

# CORS_ORIGIN_WHITELIST = [
#     "http://host.docker.internal:8000",
#     "localhost"
# ]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'atc_site/frontend/templates/')],
        'APP_DIRS': True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                'django.template.context_processors.request',  # Required for allauth
                'django.contrib.auth.context_processors.auth',  # Required for django_two_factor_auth
            ],
        },
    },
]

print("BASE_DIR:", BASE_DIR)
print("TEMPLATES DIR:", os.path.join(BASE_DIR, 'atc_site/frontend/templates/'))

WSGI_APPLICATION = "atc_site.wsgi.application"
ASGI_APPLICATION = 'atc_site.asgi.application'

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
        "HOST": "localhost",
        "PORT": PORT,
    }
}

# Add the following to your AUTHENTICATION_BACKENDS setting
# AUTHENTICATION_BACKENDS = (
#     'django.contrib.auth.backends.ModelBackend',
#     'allauth.account.auth_backends.AuthenticationBackend',
# )


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

AUTH_USER_MODEL = 'atc_site.CustomUser'

# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

APPEND_SLASH=False

SITE_ID = 1

# celery
CELERY_BROKER_URL = config("CELERY_BROKER_URL")
CELERY_RESULT_BACKEND = config("REDIS_BACKEND")

# Redis Cache
# Redis Cache
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": config("REDIS_BACKEND"),
    },
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}

# Django Channels
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [config("REDIS_BACKEND")],
        },
    },
}

# Chatterbot
CHATTERBOT = {
    "name": "User Support Bot",
    "logic_adapters": [
        "chatterbot.logic.BestMatch",
    ],
}

#Email settings
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'atc_site/frontend/static'),
]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


print("STATIC_ROOT:", STATIC_ROOT)