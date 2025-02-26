from datetime import datetime
from logger import setup_logger

# Initialize logging
logger = setup_logger()

def get_current_timestamp():
    """
    Get the current timestamp in the format "YYYY-MM-DD HH:MM:SS".

    Returns:
        str: Current timestamp.
    """
    try:
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    except Exception as e:
        logger.error(f"Error getting current timestamp: {e}")
        return ""

def format_timestamp(timestamp):
    """
    Format a timestamp into a human-readable string.

    Args:
        timestamp (str): Timestamp in the format "YYYY-MM-DD HH:MM:SS".

    Returns:
        str: Formatted timestamp (e.g., "January 1, 2023, 12:00 PM").
    """
    try:
        dt = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
        return dt.strftime("%B %d, %Y, %I:%M %p")
    except Exception as e:
        logger.error(f"Error formatting timestamp {timestamp}: {e}")
        return ""