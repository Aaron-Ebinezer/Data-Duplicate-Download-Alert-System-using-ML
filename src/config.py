import os

# Configuration settings
DOWNLOAD_FOLDER = os.path.join(os.path.expanduser("~"), "Downloads")  # Default download folder
DATABASE_PATH = os.path.join(os.path.dirname(__file__), "scda.db")  # SQLite database path
WINDOWS_DEFENDER_ENABLED = True  # Enable/disable Windows Defender integration
AI_MODEL_PATH = os.path.join(os.path.dirname(__file__), "ai_model.pth")  # Path to AI model (if applicable)

# Logging configuration
LOG_FILE = os.path.join(os.path.dirname(__file__), "scda.log")  # Log file path
LOG_LEVEL = "INFO"  # Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)