import tkinter as tk
from tkinter import ttk, messagebox
from logger import setup_logger
from database.db_handler import DatabaseHandler

# Initialize logging
logger = setup_logger()

class SCDAUI:
    def __init__(self, root):
        """
        Initialize the main UI window.

        Args:
            root (tk.Tk): Root window.
        """
        self.root = root
        self.root.title("SCDA - Smart Collaborative Download Assistant")
        self.root.geometry("800x600")

        # Initialize database handler
        self.db_handler = DatabaseHandler()

        # Create UI components
        self._create_widgets()

    def _create_widgets(self):
        """
        Create and layout UI components.
        """
        # Frame for download history
        self.history_frame = ttk.LabelFrame(self.root, text="Download History")
        self.history_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Treeview for displaying download records
        self.tree = ttk.Treeview(
            self.history_frame,
            columns=("ID", "Filename", "File Hash", "File Size", "MIME Type", "Download URL", "Timestamp"),
            show="headings"
        )
        self.tree.heading("ID", text="ID")
        self.tree.heading("Filename", text="Filename")
        self.tree.heading("File Hash", text="File Hash")
        self.tree.heading("File Size", text="File Size")
        self.tree.heading("MIME Type", text="MIME Type")
        self.tree.heading("Download URL", text="Download URL")
        self.tree.heading("Timestamp", text="Timestamp")
        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Load download history
        self._load_download_history()

        # Buttons
        self.button_frame = ttk.Frame(self.root)
        self.button_frame.pack(fill=tk.X, padx=10, pady=10)

        self.refresh_button = ttk.Button(self.button_frame, text="Refresh", command=self._load_download_history)
        self.refresh_button.pack(side=tk.LEFT, padx=5)

        self.delete_button = ttk.Button(self.button_frame, text="Delete", command=self._delete_selected_record)
        self.delete_button.pack(side=tk.LEFT, padx=5)

    def _load_download_history(self):
        """
        Load download history from the database and display it in the Treeview.
        """
        # Clear existing records
        for row in self.tree.get_children():
            self.tree.delete(row)

        # Fetch records from the database
        try:
            self.db_handler.cursor.execute("SELECT * FROM downloads")
            rows = self.db_handler.cursor.fetchall()

            # Insert records into the Treeview
            for row in rows:
                self.tree.insert("", tk.END, values=row)
        except Exception as e:
            logger.error(f"Error loading download history: {e}")
            messagebox.showerror("Error", "Failed to load download history.")

    def _delete_selected_record(self):
        """
        Delete the selected download record from the database.
        """
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "No record selected.")
            return

        # Get the ID of the selected record
        record_id = self.tree.item(selected_item, "values")[0]

        # Delete the record from the database
        try:
            self.db_handler.cursor.execute("DELETE FROM downloads WHERE id = ?", (record_id,))
            self.db_handler.connection.commit()
            logger.info(f"Deleted download record with ID: {record_id}")
            self._load_download_history()  # Refresh the history
        except Exception as e:
            logger.error(f"Error deleting download record: {e}")
            messagebox.showerror("Error", "Failed to delete the selected record.")

    def close(self):
        """
        Close the database connection and the UI.
        """
        self.db_handler.close()
        self.root.destroy()

def start_ui():
    """
    Start the UI application.
    """
    root = tk.Tk()
    app = SCDAUI(root)
    root.protocol("WM_DELETE_WINDOW", app.close)
    root.mainloop()