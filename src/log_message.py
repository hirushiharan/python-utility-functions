"""
This script provides a simple logging mechanism that supports logging messages 
with different levels (INFO, WARNING, ERROR) to both the console and a log file 
in JSON format. It also includes log file rotation to manage log file size.

Functions:
- create_log_file(): Ensures the log file exists by creating it if it does not.
- rotate_log_file(): Rotates the log file when its size exceeds the maximum allowed size (5 MB).
- log(message: str, level: str = INFO): Logs messages with a timestamp and a specific log level.

Constants:
- INFO: Log level for informational messages.
- WARNING: Log level for warning messages.
- ERROR: Log level for error messages.
- MAX_LOG_SIZE: Maximum size of the log file before rotation (5 MB).
- LOG_FILE: Path to the log file.

Usage:
- Call the log function with a message and an optional log level to log messages.
- The script will automatically handle log file creation and rotation.

Note:
- Ensure the LOG_FILE path is correctly set to the desired log file location.
- The log messages are written in JSON format to facilitate easy parsing.
"""

import json
from datetime import datetime
from pathlib import Path

# Constants for log levels and log file management
INFO = "INFO"
WARNING = "WARNING"
ERROR = "ERROR"
MAX_LOG_SIZE = 5 * 1024 * 1024  # 5 MB
LOG_FILE = "logs/application.log"

def create_log_file():
    """
    Ensures the log file exists.

    This function checks if the log file specified by LOG_FILE exists. 
    If it does not, the function creates an empty log file.
    
    Returns:
        None
    """
    if not Path(LOG_FILE).exists():
        Path(LOG_FILE).parent.mkdir(parents=True, exist_ok=True)
        with open(LOG_FILE, "x") as file:
            file.close()

def rotate_log_file():
    """
    Rotates the log file when its size exceeds the maximum allowed size.

    This function checks if the current log file exceeds the predefined maximum
    size (5 MB). If it does, the function renames the current log file to include
    a timestamp in its name and retains it as an old log file. The timestamp
    format used is 'YYYYMMDD_HHMMSS' to ensure uniqueness and chronological
    sorting of old log files.

    The log file is renamed with the format: 'YYYYMMDD_HHMMSS-application.log'.

    Returns:
        None
    """
    if Path(LOG_FILE).exists() and Path(LOG_FILE).stat().st_size > MAX_LOG_SIZE:
        # Generate a timestamp for the old log file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        new_log_file_name = f"{timestamp}-{LOG_FILE}"
        
        # Rotate the log file
        Path(LOG_FILE).rename(new_log_file_name)

def log(message: str, level: str = INFO) -> None:
    """
    Logs messages with a timestamp and a specific log level.
    Supports logging to both the console and a file in JSON format.

    Args:
        message (str): The message to log.
        level (str): The log level (e.g., INFO, WARNING, ERROR).
    
    Returns:
        None
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_message = {
        "timestamp": timestamp,
        "level": level,
        "message": message
    }
    log_message_str = json.dumps(log_message)
    
    # Print log message to the console
    print(f"{timestamp} [{level}] {message}")
    
    # Rotate log file if necessary
    rotate_log_file()
    create_log_file()

    # Write log message to the log file
    with open(LOG_FILE, "a") as log_file:
        log_file.write(log_message_str + "\n")
