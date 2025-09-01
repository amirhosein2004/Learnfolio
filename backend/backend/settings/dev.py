import os
from .base import *

# ---------------------------------------------
# Database configuration for development
#
# By default, uses SQLite for local development.
# To use PostgreSQL, set the following environment variables:
#   DB_ENGINE=django.db.backends.postgresql
#   POSTGRES_DB, POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_HOST, POSTGRES_PORT
# If DB_ENGINE is not set, SQLite will be used with db.sqlite3 in BASE_DIR.
# ---------------------------------------------

DB_ENGINE = os.getenv('DB_ENGINE', 'django.db.backends.sqlite3')

if DB_ENGINE == 'django.db.backends.sqlite3':
    # SQLite configuration (default for development)
    DATABASES = {
        'default': {
            'ENGINE': DB_ENGINE,
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
else:
    # PostgreSQL configuration (if environment variables are set)
    DATABASES = {
        'default': {
            'ENGINE': DB_ENGINE,
            'NAME': os.getenv("POSTGRES_DB"),
            'USER': os.getenv("POSTGRES_USER"),
            'PASSWORD': os.getenv("POSTGRES_PASSWORD"),
            'HOST': os.getenv("POSTGRES_HOST", "db"),
            'PORT': os.getenv("POSTGRES_PORT", "5432"),
        }
    }

# Allow all origins (only for development)
CORS_ALLOW_ALL_ORIGINS = True 

# Media files configuration
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'