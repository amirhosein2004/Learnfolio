import os

from django.core.wsgi import get_wsgi_application

from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from a .env file located in the project's root directory.
BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR.parent / '.env')

# Read the DJANGO_ENV environment variable to determine the current environment (e.g., 'dev', 'prod').
# If DJANGO_ENV is not set, default to 'dev'.
env = os.getenv('DJANGO_ENV', 'dev')  

# Set the Django settings module based on the environment.
# For example, this could result in 'backend.settings.dev' or 'backend.settings.prod'.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', f'backend.settings.{env}')

application = get_wsgi_application()
