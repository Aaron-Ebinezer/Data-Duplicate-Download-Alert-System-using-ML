import requests
from logger import setup_logger

# Initialize logging
logger = setup_logger()

def upload_file_to_cloud(file_path, cloud_url):
    """
    Upload a file to a cloud storage service.

    Args:
        file_path (str): Path to the file.
        cloud_url (str): URL of the cloud storage service.

    Returns:
        bool: True if the upload was successful, False otherwise.
    """
    try:
        with open(file_path, "rb") as f:
            response = requests.post(cloud_url, files={"file": f})
            if response.status_code == 200:
                logger.info(f"File uploaded successfully: {file_path}")
                return True
            else:
                logger.error(f"Failed to upload file: {response.status_code} - {response.text}")
                return False
    except Exception as e:
        logger.error(f"Error uploading file {file_path}: {e}")
        return False