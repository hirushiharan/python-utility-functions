from datetime import datetime, timezone, timedelta

def get_current_time():
    """Return the current time in IST (+5:30)."""
    current_time = datetime.now(timezone(timedelta(hours=5, minutes=30)))
    return current_time