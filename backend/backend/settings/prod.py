from .base import *
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration
from sentry_sdk.integrations.logging import LoggingIntegration

# Database configuration(postgres)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv("POSTGRES_DB"),
        'USER': os.getenv("POSTGRES_USER"),
        'PASSWORD': os.getenv("POSTGRES_PASSWORD"),
        'HOST': os.getenv("POSTGRES_HOST", "db"),
        'PORT': os.getenv("POSTGRES_PORT", "5432"),
    }
}

STATIC_ROOT = BASE_DIR / 'staticfiles'

# Allow origins (only for product)
CORS_ALLOWED_ORIGINS = [
    "https://myfrontend.com",
    "https://admin.myfrontend.com",
]

# Sentry settings
# Initialize Sentry for error tracking and performance monitoring
sentry_sdk.init(
    dsn=os.getenv("SENTRY_DSN"),
    integrations=[
        # Integrate logging to capture ERROR level logs and send them to Sentry
        LoggingIntegration(
            level="ERROR",          # Capture logs from ERROR level and above
            event_level="ERROR"     # Send ERROR level logs to Sentry as events
        ),
    ],
    send_default_pii=True,          # Send user information (PII) if available
    environment="Production",       # Set environment name for Sentry
    traces_sample_rate=0.1,         # Sample 10% of transactions for performance monitoring
)