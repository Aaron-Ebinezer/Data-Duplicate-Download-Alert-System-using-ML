import os
import subprocess
import logging
from config import WINDOWS_DEFENDER_ENABLED
from logger import setup_logger

logger = setup_logger()

def initialize_antivirus():
    """
    Initialize the antivirus scanner.
    """
    logger.info("Initializing antivirus scanner...")

    if not WINDOWS_DEFENDER_ENABLED:
        logger.warning("Windows Defender is disabled in configuration.")
        return False

    # Check if MpCmdRun.exe exists
    defender_path = "C:\\Program Files\\Windows Defender\\MpCmdRun.exe"
    if not os.path.exists(defender_path):
        logger.error(f"Windows Defender executable not found at {defender_path}")
        return False

    try:
        # Check if Windows Defender is available
        result = subprocess.run([defender_path, "-?"], capture_output=True, text=True)
        if result.returncode == 0:
            logger.info("Windows Defender is available and ready to use.")
            return True
        else:
            logger.error("Windows Defender is not available on this system.")
            return False
    except Exception as e:
        logger.error(f"Error initializing antivirus: {e}")
        return False

def scan_file(file_path):
    """
    Scan a file using Windows Defender.

    Args:
        file_path (str): Path to the file to be scanned.

    Returns:
        str: Scan result ("clean", "infected", or "error").
    """
    defender_path = "C:\\Program Files\\Windows Defender\\MpCmdRun.exe"
    if not os.path.exists(file_path):
        logger.error(f"File not found: {file_path}")
        return "error"

    try:
        # Run Windows Defender scan
        logger.info(f"Scanning file: {file_path}")
        result = subprocess.run(
            ["C:\\Program Files\\Windows Defender\\MpCmdRun.exe", "-Scan", "-ScanType", "3", "-File", file_path],
            capture_output=True,
            text=True
        )

        # Parse scan result
        if "No threats detected" in result.stdout:
            logger.info(f"File is clean: {file_path}")
            return "clean"
        elif "Threats detected" in result.stdout:
            logger.warning(f"File is infected: {file_path}")
            return "infected"
        else:
            logger.error(f"Scan failed for file: {file_path}")
            return "error"

    except Exception as e:
        logger.error(f"Error during scan: {e}")
        return "error"