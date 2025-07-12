from dotenv import load_dotenv
from pathlib import Path
import os

# Define the base directory of the project
BASE_DIR = Path(__file__).resolve().parent.parent

# Load environment variables from a .env file located at the project root
load_dotenv(BASE_DIR.parent / '.env')

# General environment variables
SECRET_KEY = os.getenv("SECRET_KEY", "insecure-default")
DEBUG = os.getenv("DEBUG", "False") == "True"
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
    'rest_framework',
    'corsheaders',
    'django_celery_beat',
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
    'accounts.backends.EmailOrPhoneBackend',  # custom backend
    'django.contrib.auth.backends.ModelBackend',  # default fallback
]

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

# Django REST Framework settings
REST_FRAMEWORK = {
    # Throttling classes to limit API request rates
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.UserRateThrottle',  # Limits for authenticated users
        'rest_framework.throttling.AnonRateThrottle',  # Limits for anonymous users
    ],
    # Throttle rates for different user types and custom actions
    'DEFAULT_THROTTLE_RATES': {
        'user': os.getenv('THROTTLE_RATE_USER', '200/hour'), # for authenticated users
        'anon': os.getenv('THROTTLE_RATE_ANON', '200/hour'), # for anonymous users
        'custom_action': os.getenv('THROTTLE_RATE_CUSTOM', '15/minute'), # for custom actions
    },
    # Custom exception handler for API errors
    'EXCEPTION_HANDLER': 'core.exceptions.exception_handlers.custom_exception_handler',
}

# Celery configuration
# Broker URL for Celery (default: RabbitMQ)
CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL', 'amqp://user:pass@rabbitmq:5672//')
# Backend for storing task results (set to None to disable result storage)
CELERY_RESULT_BACKEND = 'rpc://'  # You can change to 'redis://' or a database backend if needed
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