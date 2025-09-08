import os
from dotenv import load_dotenv
from pathlib import Path

# Root directory of the project backend(3 levels up from this file)
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Create a logs directory if it doesn't exist
LOGS_DIR = BASE_DIR / "logs"
LOGS_DIR.mkdir(exist_ok=True)

# Load environment variables from a .env file located at the project root
load_dotenv(BASE_DIR.parent / '.env')

# 🔍 Determine current environment: development or production
ENV = os.getenv("DJANGO_ENV", "dev").lower()
IS_DEV = ENV == "dev"
LOG_LEVEL = "DEBUG" if IS_DEV else "INFO"

# Apps that require separate log files
APPS = ["accounts", "core", "blog", "education"]

def make_handler(filename):
    """
    Creates logging handler.

    Args:
        filename (str): The log file name.

    Returns:
        dict: Configuration for a log handler that:
              - Saves logs to the given file.
              - Rotates the file every midnight.
              - Keeps logs for 7 days before deleting old ones.
              - Uses the 'verbose' format and proper encoding.
    """
    return {
        "class": "logging.handlers.TimedRotatingFileHandler",
        "filename": str(LOGS_DIR / filename),
        "when": "midnight",
        "backupCount": 7,
        "formatter": "verbose",
        "level": LOG_LEVEL,
        "encoding": "utf-8",
    }

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,

    # Formatters define how logs will look
    "formatters": {
        "verbose": {
            "format": "[{asctime}] [{levelname}] {name} - {message}",
            "style": "{",
        },
    },

    # Handlers define where logs go (console, files, etc.)
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "verbose",
            "level": LOG_LEVEL,
        },
        "django_file": make_handler("django.log"),
        "root_file": make_handler("root.log"),
        # Create individual file handlers for each app
        **{f"{app}_file": make_handler(f"{app}.log") for app in APPS},
    },

    # Loggers determine which handlers to use for each source
    "loggers": {
        "django": {
            "handlers": (["console"] if IS_DEV else []) + ["django_file"],
            "level": LOG_LEVEL,
            "propagate": True,
        },
        **{
            app: {
                "handlers": (["console"] if IS_DEV else []) + [f"{app}_file"],
                "level": LOG_LEVEL,
                "propagate": True, # Allow messages to propagate to higher-level loggers (usually root)
            } for app in APPS
        }
    },

    # Root logger (fallback for all other logs)
    "root": {
        "handlers": (["console"] if IS_DEV else []) + ["root_file"],
        "level": LOG_LEVEL,
    },
}
