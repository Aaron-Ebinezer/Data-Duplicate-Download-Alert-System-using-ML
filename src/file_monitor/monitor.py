import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from config import DOWNLOAD_FOLDER
from logger import setup_logger

# Initialize logging
logger = setup_logger()

class DownloadHandler(FileSystemEventHandler):
    def __init__(self, callback):
        """
        Initialize the event handler with a callback function.

        Args:
            callback (function): Function to call when a new file is detected.
        """
        self.callback = callback

    def on_created(self, event):
        """
        Handle file creation events.

        Args:
            event (FileSystemEvent): Event object containing details about the file.
        """
        if not event.is_directory:
            logger.info(f"New file detected: {event.src_path}")
            self.callback(event.src_path)

    def on_modified(self, event):
        """
        Handle file modification events.

        Args:
            event (FileSystemEvent): Event object containing details about the file.
        """
        if not event.is_directory:
            logger.info(f"File modified: {event.src_path}")
            self.callback(event.src_path)

def start_file_monitoring(callback):
    """
    Start monitoring the download folder for new files and modifications.

    Args:
        callback (function): Function to call when a new file is detected.
    """
    event_handler = DownloadHandler(callback)
    observer = Observer()
    observer.schedule(event_handler, DOWNLOAD_FOLDER, recursive=True)
    observer.start()
    logger.info(f"Started monitoring download folder: {DOWNLOAD_FOLDER}")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()