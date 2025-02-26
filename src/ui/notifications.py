import tkinter as tk
from tkinter import messagebox
from logger import setup_logger

# Initialize logging
logger = setup_logger()

def show_notification(message):
    """
    Show a notification to the user.

    Args:
        message (str): The message to display.
    """
    logger.info(f"Showing notification: {message}")
    messagebox.showinfo("Notification", message)

def show_error(message):
    """
    Show an error message to the user.

    Args:
        message (str): The error message to display.
    """
    logger.error(f"Showing error: {message}")
    messagebox.showerror("Error", message)

def show_warning(message):
    """
    Show a warning message to the user.

    Args:
        message (str): The warning message to display.
    """
    logger.warning(f"Showing warning: {message}")
    messagebox.showwarning("Warning", message)