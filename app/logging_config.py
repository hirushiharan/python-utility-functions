import logging
import logging.config
import sys
import os
from app.utils.time import get_current_time

# Get current date in YYYYMMDD format
current_date = get_current_time().strftime("%Y%m%d")

# Define the logs directory path
logs_dir = "logs"

"""
1. DEBUG (10) – Detailed information, typically useful for diagnosing problems.
2. INFO (20) – Confirmation that things are working as expected.
3. WARNING (30) – An indication that something unexpected happened or a potential issue exists.
4. ERROR (40) – A more serious problem that caused some functionality to fail.
5. CRITICAL (50) – A severe error indicating that the program might be unable to continue running.
"""

LOGGING_LEVEL_ROOT = "DEBUG"
LOGGING_LEVEL_CONSOLE = "DEBUG"
LOGGING_LEVEL_FILE = "DEBUG"

# Define logging configuration
LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {module} {message}",
            "style": "{",
        },
        "simple": {
            "format": "{levelname} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "level": LOGGING_LEVEL_CONSOLE,
            "class": "logging.StreamHandler",
            "formatter": "verbose",
            "stream": sys.stdout,  # Output to console
        },
        "file": {
            "level": LOGGING_LEVEL_FILE,
            "class": "logging.handlers.TimedRotatingFileHandler",
            "formatter": "verbose",
            "filename": os.path.join(logs_dir, f"api-log-{current_date}.log"),  # Log to a file with date
            "when": "midnight",  # Rotate at midnight
            "backupCount": 30,   # Keep 30 days of logs
        },
    },
    "root": {
        "handlers": ["console", "file"],
        "level": LOGGING_LEVEL_ROOT,
    },
}

def setup_logging():
    # Ensure the logs directory exists
    if not os.path.exists(logs_dir):
        os.makedirs(logs_dir)
    
    # Update the filename with the current date
    LOGGING_CONFIG['handlers']['file']['filename'] = os.path.join(logs_dir, f"api-log-{get_current_time().strftime('%Y%m%d')}.log")

    
    logging.config.dictConfig(LOGGING_CONFIG)
    logger = logging.getLogger(__name__)
    logger.info("Logging is set up.")
