import sqlite3
import logging
from config import DATABASE_PATH
from logger import setup_logger

# Initialize logging
logger = setup_logger()

class DatabaseHandler:
    def __init__(self):
        """
        Initialize the database handler.
        """
        self.connection = sqlite3.connect(DATABASE_PATH)
        self.cursor = self.connection.cursor()
        self._initialize_schema()

    def _initialize_schema(self):
        """
        Initialize the database schema if it doesn't exist.
        """
        try:
            with open("src/database/schema.sql", "r") as f:
                self.cursor.executescript(f.read())
            self.connection.commit()
            logger.info("Database schema initialized.")
        except Exception as e:
            logger.error(f"Error initializing database schema: {e}")

    def insert_download_record(self, filename, file_hash, file_size, mime_type, download_url):
        """
        Insert a new download record into the database.

        Args:
            filename (str): Name of the downloaded file.
            file_hash (str): SHA-256 hash of the file.
            file_size (int): Size of the file in bytes.
            mime_type (str): MIME type of the file.
            download_url (str): URL from which the file was downloaded.

        Returns:
            bool: True if the record was inserted successfully, False otherwise.
        """
        try:
            self.cursor.execute(
                "INSERT INTO downloads (filename, file_hash, file_size, mime_type, download_url) VALUES (?, ?, ?, ?, ?)",
                (filename, file_hash, file_size, mime_type, download_url)
            )
            self.connection.commit()
            logger.info(f"Inserted download record for file: {filename}")
            return True
        except Exception as e:
            logger.error(f"Error inserting download record: {e}")
            return False

    def get_download_record_by_hash(self, file_hash):
        """
        Retrieve a download record by file hash.

        Args:
            file_hash (str): SHA-256 hash of the file.

        Returns:
            dict: Download record if found, otherwise None.
        """
        try:
            self.cursor.execute("SELECT * FROM downloads WHERE file_hash = ?", (file_hash,))
            row = self.cursor.fetchone()
            if row:
                return {
                    "id": row[0],
                    "filename": row[1],
                    "file_hash": row[2],
                    "file_size": row[3],
                    "mime_type": row[4],
                    "download_url": row[5],
                    "timestamp": row[6]
                }
            else:
                return None
        except Exception as e:
            logger.error(f"Error retrieving download record by hash: {e}")
            return None

    def get_download_record_by_filename(self, filename):
        """
        Retrieve a download record by filename.

        Args:
            filename (str): Name of the file.

        Returns:
            dict: Download record if found, otherwise None.
        """
        try:
            self.cursor.execute("SELECT * FROM downloads WHERE filename = ?", (filename,))
            row = self.cursor.fetchone()
            if row:
                return {
                    "id": row[0],
                    "filename": row[1],
                    "file_hash": row[2],
                    "file_size": row[3],
                    "mime_type": row[4],
                    "download_url": row[5],
                    "timestamp": row[6]
                }
            else:
                return None
        except Exception as e:
            logger.error(f"Error retrieving download record by filename: {e}")
            return None

    def close(self):
        """
        Close the database connection.
        """
        self.connection.close()
        logger.info("Database connection closed.")