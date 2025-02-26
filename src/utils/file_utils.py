import os
import hashlib
from logger import setup_logger

# Initialize logging
logger = setup_logger()

def generate_file_hash(file_path):
    """
    Generate a SHA-256 hash for a file.

    Args:
        file_path (str): Path to the file.

    Returns:
        str: SHA-256 hash of the file.
    """
    hasher = hashlib.sha256()
    try:
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hasher.update(chunk)
        return hasher.hexdigest()
    except Exception as e:
        logger.error(f"Error generating hash for {file_path}: {e}")
        return None

def validate_file(file_path):
    """
    Validate if a file exists and is accessible.

    Args:
        file_path (str): Path to the file.

    Returns:
        bool: True if the file is valid, False otherwise.
    """
    try:
        return os.path.exists(file_path) and os.path.isfile(file_path)
    except Exception as e:
        logger.error(f"Error validating file {file_path}: {e}")
        return False

def get_file_size(file_path):
    """
    Get the size of a file in bytes.

    Args:
        file_path (str): Path to the file.

    Returns:
        int: Size of the file in bytes.
    """
    try:
        return os.path.getsize(file_path)
    except Exception as e:
        logger.error(f"Error getting file size for {file_path}: {e}")
        return 0

def get_file_extension(file_path):
    """
    Get the file extension from a file path.

    Args:
        file_path (str): Path to the file.

    Returns:
        str: File extension (e.g., ".txt").
    """
    try:
        return os.path.splitext(file_path)[1]
    except Exception as e:
        logger.error(f"Error getting file extension for {file_path}: {e}")
        return ""