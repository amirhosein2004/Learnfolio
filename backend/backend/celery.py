import os
from celery import Celery
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from a .env file located in the project's root directory.
BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR.parent / '.env')

# Get the environment type (dev, prod, etc.)
env = os.getenv('DJANGO_ENV', 'dev')

# Set Django settings module according to the environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', f'backend.settings.{env}')

# Create Celery application instance
app = Celery('backend')

# Load Celery config from Django settings with 'CELERY' namespace
app.config_from_object('django.conf:settings', namespace='CELERY')

# Auto-discover tasks from installed Django apps
app.autodiscover_tasks()