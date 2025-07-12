import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from a .env file located in the project's root directory.
BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR.parent / '.env')

def main():
    """Run administrative tasks."""
    # Read the DJANGO_ENV environment variable to determine the current environment (e.g., 'dev', 'prod').
    # If DJANGO_ENV is not set, default to 'dev'.
    env = os.getenv('DJANGO_ENV', 'dev')

    # Set the Django settings module based on the environment.
    # For example, this could result in 'backend.settings.dev' or 'backend.settings.prod'.
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', f'backend.settings.{env}')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
