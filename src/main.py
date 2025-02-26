import logging
from file_monitor.monitor import start_file_monitoring
from file_monitor.event_handler import handle_file_event
from ai_duplicate_detection.model import AIDuplicateDetector
from antivirus_scan.scan import initialize_antivirus
from database.db_handler import DatabaseHandler
from ui.main_ui import start_ui
from logger import setup_logger

# Initialize logging
logger = setup_logger()

def main():
    """
    Main function to start the SCDA application.
    """
    logger.info("Starting SCDA...")

    # Initialize modules
    db_handler = DatabaseHandler()
    detector = AIDuplicateDetector()
    initialize_antivirus()

    # Start file monitoring
    start_file_monitoring(handle_file_event)

    # Start UI
    start_ui()

    # Close the database connection when done
    db_handler.close()
    logger.info("SCDA stopped.")

if __name__ == "__main__":
    main()