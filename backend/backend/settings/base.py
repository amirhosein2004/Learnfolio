from dotenv import load_dotenv
from pathlib import Path
import os
from .logging_config import LOGGING_CONFIG as CUSTOM_LOGGING  
from datetime import timedelta

# Define the base directory of the project
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Load environment variables from a .env file located at the project root
load_dotenv(BASE_DIR.parent / '.env')

# General environment variables
SECRET_KEY = os.getenv("SECRET_KEY", "insecure-default")
DEBUG = os.getenv("DEBUG", "false") == "true"
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '*').split(',') 


# Define Installed apps for the Django project
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Custom apps
    'accounts',
    'core',

    # third party
    'rest_framework',         # Enables Django REST API support
    'corsheaders',            # Handles Cross-Origin Resource Sharing (CORS)
    'django_celery_beat',     # Periodic task scheduler for Celery
    'drf_spectacular',        # Auto-generates OpenAPI schema and Swagger docs
    'rest_framework_simplejwt', # JWT authentication for REST framework
    'rest_framework_simplejwt.token_blacklist', # Token blacklist for JWT authentication
]

# Middleware configuration
MIDDLEWARE = [
    # Third-party middleware
    'corsheaders.middleware.CorsMiddleware', # CORS middleware for handling cross-origin requests

    # Default Django middleware
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Root URL configuration
ROOT_URLCONF = 'backend.urls'

# Template settings
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# WSGI application
WSGI_APPLICATION = 'backend.wsgi.application'

# Password validation settings
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Localization settings
LANGUAGE_CODE = os.getenv('LANGUAGE_CODE', 'en-us')
TIME_ZONE = os.getenv('TIME_ZONE', 'UTC')
USE_I18N = os.getenv('USE_I18N', 'False') == 'True'
USE_TZ = os.getenv('USE_TZ', 'False') == 'True'

STATIC_URL = 'static/'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Custom user model
AUTH_USER_MODEL = 'accounts.User'

# Authentication backends configuration
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',  # default fallback
]

# Redis cache configuration
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": os.getenv('REDIS_LOCATION'),  # name service redis in docker-compose
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}

#********************************************************************************#

# For Kavenegar SMS service
KAVENEGAR_API_KEY = os.getenv('KAVENEGAR_API_KEY')

# Email configuration
DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL', "amirhoosenbabai82@gmail.com")
EMAIL_BACKEND = os.getenv('EMAIL_BACKEND', 'django.core.mail.backends.console.EmailBackend')
EMAIL_HOST = os.getenv('EMAIL_HOST', 'smtp.gmail.com')
EMAIL_PORT = int(os.getenv('EMAIL_PORT', 587))
EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS', 'True') == 'True'
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER', 'amirhoosenbabai82@gmail.com')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD', None)

# Celery configuration
# Broker URL for Celery (default: RabbitMQ)
CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL', 'amqp://user:pass@rabbitmq:5672//')
# Backend for storing task results (set to None to disable result storage)
CELERY_RESULT_BACKEND = os.getenv('CELERY_RESULT_BACKEND')
# Accepted content types for tasks
CELERY_ACCEPT_CONTENT = ['json']
# Serialization format for tasks and results
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
# Retry broker connection on startup if it fails
CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True

# Celery Beat configuration
# Use the Django database as the scheduler for periodic Celery tasks
CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'

# LOGGING configuration
# Tells Django to use the `dictConfig` function from the `logging.config` module to configure logging
LOGGING_CONFIG = "logging.config.dictConfig"
LOGGING = CUSTOM_LOGGING

# Turnstile Captcha configuration
TURNSTILE_ENABLED = os.getenv("TURNSTILE_ENABLED", "false").lower() == "true"
TURNSTILE_SECRET_KEY = os.getenv("TURNSTILE_SECRET_KEY")

#********************************************************************************#

# Django REST Framework settings
REST_FRAMEWORK = {
    # Throttling
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.UserRateThrottle',
        'rest_framework.throttling.AnonRateThrottle',
    ],
    'DEFAULT_THROTTLE_RATES': {
        'user': os.getenv('THROTTLE_RATE_USER', '200/hour'),
        'anon': os.getenv('THROTTLE_RATE_ANON', '200/hour'),
        'custom_action': os.getenv('THROTTLE_RATE_CUSTOM', '15/minute'),
        'resend_otp_or_link': '3/minute',
    },

    # Exception handling
    'EXCEPTION_HANDLER': 'core.exceptions.exception_handlers.custom_exception_handler',

    # Schema / documentation
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',

    # JWT authentication
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}

# Simple JWT settings
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=15),   # Short lifetime for increased security
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
}
