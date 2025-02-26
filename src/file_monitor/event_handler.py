import os
from logger import setup_logger
from database.db_handler import DatabaseHandler
from utils.file_utils import generate_file_hash

# Initialize logging
logger = setup_logger()

def handle_file_event(file_path):
    """
    Handle file events (new downloads or modifications).

    Args:
        file_path (str): Path to the file.
    """
    logger.info(f"Handling file event for: {file_path}")

    # Generate file hash
    file_hash = generate_file_hash(file_path)
    if not file_hash:
        logger.error(f"Failed to generate hash for file: {file_path}")
        return

    # Check for duplicates in the database
    db_handler = DatabaseHandler()
    duplicate_record = db_handler.get_download_record_by_hash(file_hash)
    if duplicate_record:
        logger.warning(f"Duplicate file found: {duplicate_record['filename']}")
    else:
        # Insert new download record
        db_handler.insert_download_record(
            filename=file_path.split("\\")[-1],  # Extract filename from path
            file_hash=file_hash,
            file_size=os.path.getsize(file_path),
            mime_type="application/octet-stream",  # Default MIME type
            download_url="local"  # Indicates a local file
        )
        logger.info(f"New file added to database: {file_path}")

    db_handler.close()