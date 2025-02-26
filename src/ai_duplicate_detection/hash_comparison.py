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

def detect_exact_duplicate(file_path, file_hashes):
    """
    Detect exact duplicates using file hashing.

    Args:
        file_path (str): Path to the file.
        file_hashes (dict): Dictionary of file hashes.

    Returns:
        str: Path to the duplicate file if found, otherwise None.
    """
    file_hash = generate_file_hash(file_path)
    if not file_hash:
        return None

    if file_hash in file_hashes:
        logger.info(f"Exact duplicate found: {file_hashes[file_hash]}")
        return file_hashes[file_hash]
    else:
        file_hashes[file_hash] = file_path
        return None