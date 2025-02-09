import os
import hashlib
import sqlite3
import logging
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QLabel, QFileDialog, QListWidget, QVBoxLayout, QMessageBox, QProgressBar
)
from PyQt5.QtCore import pyqtSignal, Qt
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from PIL import Image
import imagehash
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from plyer import notification

# Logging configuration
logging.basicConfig(filename="duplicate_checker.log", level=logging.ERROR, format="%(asctime)s - %(levelname)s - %(message)s")

DB_NAME = "files_db.sqlite"

def initialize_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS files (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT NOT NULL,
            filepath TEXT UNIQUE NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

class FileEventHandler(FileSystemEventHandler):
    def __init__(self, app):
        self.app = app

    def on_created(self, event):
        if not event.is_directory:
            self.app.file_detected.emit(event.src_path)

class DuplicateFileChecker(QWidget):
    file_detected = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.initUI()
        self.target_dir = None
        initialize_db()
        self.observer = Observer()
        self.file_detected.connect(self.check_new_file)

    def initUI(self):
        self.setWindowTitle("Duplicate File Checker")
        self.setGeometry(100, 100, 600, 400)

        self.label = QLabel("Select a target directory:", self)
        self.select_btn = QPushButton("Choose Directory", self)
        self.check_btn = QPushButton("Check for Duplicates", self)
        self.clear_btn = QPushButton("Clear Results", self)
        self.delete_btn = QPushButton("Delete Selected Duplicates", self)
        self.result_list = QListWidget(self)
        self.progress_bar = QProgressBar(self)

        self.select_btn.clicked.connect(self.choose_directory)
        self.check_btn.clicked.connect(self.check_duplicates)
        self.clear_btn.clicked.connect(self.clear_results)
        self.delete_btn.clicked.connect(self.delete_duplicates)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.select_btn)
        layout.addWidget(self.check_btn)
        layout.addWidget(self.clear_btn)
        layout.addWidget(self.delete_btn)
        layout.addWidget(self.result_list)
        layout.addWidget(self.progress_bar)
        self.setLayout(layout)

    def choose_directory(self):
        dir_name = QFileDialog.getExistingDirectory(self, "Select Directory")
        if dir_name:
            self.target_dir = dir_name
            self.label.setText(f"Target Directory: {self.target_dir}")
            self.start_monitoring()

    def check_duplicates(self):
        if not self.target_dir:
            QMessageBox.warning(self, "Error", "Please select a directory first!")
            return

        self.result_list.clear()
        self.progress_bar.setValue(0)

        existing_files = self.get_existing_filenames()
        file_contents = {}
        text_files = []
        image_files = []

        # Count total files for progress bar
        total_files = sum([len(files) for _, _, files in os.walk(self.target_dir)])
        processed_files = 0

        for root, _, files in os.walk(self.target_dir):
            for file in files:
                file_path = os.path.join(root, file)
                file_ext = os.path.splitext(file)[1].lower()

                if file in existing_files:
                    self.result_list.addItem(f"Duplicate Name: {file}")

                if file_ext in ['.txt', '.md', '.log']:
                    text_files.append(file_path)
                elif file_ext in ['.jpg', '.jpeg', '.png', '.gif']:
                    image_files.append(file_path)

                file_contents[file_path] = self.get_file_hash(file_path)
                self.store_file_in_db(file, file_path)

                # Update progress bar
                processed_files += 1
                self.progress_bar.setValue(int((processed_files / total_files) * 100))

        self.check_text_similarity(text_files)
        self.check_image_similarity(image_files)

    def check_text_similarity(self, text_files):
        if len(text_files) < 2:
            return

        texts = []
        for file in text_files:
            try:
                with open(file, "r", errors="ignore") as f:
                    texts.append(f.read())
            except Exception as e:
                logging.error(f"Error reading file {file}: {e}")

        vectorizer = TfidfVectorizer().fit_transform(texts)
        similarities = cosine_similarity(vectorizer)

        for i in range(len(text_files)):
            for j in range(i + 1, len(text_files)):
                if similarities[i, j] > 0.85:
                    self.result_list.addItem(f"Similar Text Files: {os.path.basename(text_files[i])} and {os.path.basename(text_files[j])}")

    def check_image_similarity(self, image_files):
        if len(image_files) < 2:
            return

        hashes = {}
        for file in image_files:
            try:
                hashes[file] = imagehash.phash(Image.open(file))
            except Exception as e:
                logging.error(f"Error processing image {file}: {e}")

        for i, file1 in enumerate(image_files):
            for j, file2 in enumerate(image_files):
                if i >= j:
                    continue
                if hashes.get(file1) and hashes.get(file2) and (hashes[file1] - hashes[file2] < 5):
                    self.result_list.addItem(f"Similar Images: {os.path.basename(file1)} and {os.path.basename(file2)}")

    def check_new_file(self, file_path):
        file_name = os.path.basename(file_path)
        existing_files = self.get_existing_filepaths()

        # Check if the file already exists
        for existing_file in existing_files:
            if os.path.basename(existing_file) == file_name:
                self.show_duplicate_alert(file_path, existing_file)
                break
        else:
            self.store_file_in_db(file_name, file_path)

    def show_duplicate_alert(self, new_file, existing_file):
        # Display a notification using plyer
        notification.notify(
            title="Duplicate File Detected",
            message=f"A file with the same name already exists:\n\n{new_file}",
            app_name="Duplicate File Checker",
            timeout=10  # Notification will disappear after 10 seconds
        )

        # Display a QMessageBox for further action
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Warning)
        msg.setWindowTitle("Duplicate File Detected")
        msg.setText(f"A file with the same name already exists:\n\n{new_file}")
        msg.setInformativeText("Do you want to open the existing file location?")
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg.button(QMessageBox.Yes).setText("Open Location")
        msg.button(QMessageBox.No).setText("Ignore")

        reply = msg.exec_()
        if reply == QMessageBox.Yes:
            self.open_file_location(existing_file)

    def open_file_location(self, file_path):
        try:
            os.startfile(os.path.dirname(file_path))  # For Windows
        except AttributeError:
            import subprocess
            subprocess.run(["open", os.path.dirname(file_path)])  # For macOS
            # subprocess.run(["xdg-open", os.path.dirname(file_path)])  # For Linux

    def get_existing_filenames(self):
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT filename FROM files")
        files = [row[0] for row in cursor.fetchall()]
        conn.close()
        return files

    def get_existing_filepaths(self):
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT filepath FROM files")
        files = [row[0] for row in cursor.fetchall()]
        conn.close()
        return files

    def store_file_in_db(self, filename, filepath):
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO files (filename, filepath) VALUES (?, ?)", (filename, filepath))
            conn.commit()
        except sqlite3.IntegrityError:
            pass
        conn.close()

    def get_file_hash(self, file_path):
        try:
            hasher = hashlib.sha256()
            with open(file_path, 'rb') as f:
                while chunk := f.read(4096):
                    hasher.update(chunk)
            return hasher.hexdigest()
        except Exception as e:
            logging.error(f"Error hashing file {file_path}: {e}")
            return None

    def start_monitoring(self):
        if self.target_dir:
            event_handler = FileEventHandler(self)
            self.observer.schedule(event_handler, path=self.target_dir, recursive=True)
            self.observer.start()

    def clear_results(self):
        self.result_list.clear()

    def delete_duplicates(self):
        selected_items = self.result_list.selectedItems()
        for item in selected_items:
            # Extract the file path from the item text
            item_text = item.text()
            
            # Handle different formats of item text
            if "Similar" in item_text or "Duplicate" in item_text:
                # Extract the file name(s) from the item text
                file_names = item_text.split(": ")[-1].split(" and ")
                for file_name in file_names:
                    file_path = os.path.join(self.target_dir, file_name)
                    self.delete_file(file_path)
            else:
                # Assume the item text is the full file path
                file_path = item_text
                self.delete_file(file_path)

    def delete_file(self, file_path):
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                self.result_list.takeItem(self.result_list.row(self.result_list.findItems(file_path, Qt.MatchExactly)[0]))
                logging.info(f"Successfully deleted {file_path}")
            else:
                logging.warning(f"File not found: {file_path}")
                QMessageBox.warning(self, "Error", f"File not found: {file_path}")
        except Exception as e:
            logging.error(f"Failed to delete {file_path}: {e}")
            QMessageBox.warning(self, "Error", f"Failed to delete {file_path}: {e}")

if __name__ == "__main__":
    app = QApplication([])
    window = DuplicateFileChecker()
    window.show()
    app.exec_()