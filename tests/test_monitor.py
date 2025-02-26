import unittest
import os
import shutil
from file_monitor.monitor import start_file_monitoring
from file_monitor.event_handler import handle_file_event
from utils.file_utils import generate_file_hash
from database.db_handler import DatabaseHandler

class TestFileMonitor(unittest.TestCase):
    def setUp(self):
        """
        Set up the test environment.
        """
        self.test_dir = "test_downloads"
        os.makedirs(self.test_dir, exist_ok=True)
        self.db_handler = DatabaseHandler()

    def tearDown(self):
        """
        Clean up the test environment.
        """
        shutil.rmtree(self.test_dir)
        self.db_handler.close()

    def test_file_monitoring(self):
        """
        Test file monitoring by creating a new file and checking if it is detected.
        """
        # Create a test file
        test_file = os.path.join(self.test_dir, "test_file.txt")
        with open(test_file, "w") as f:
            f.write("This is a test file.")

        # Simulate file monitoring
        handle_file_event(test_file)

        # Check if the file was added to the database
        file_hash = generate_file_hash(test_file)
        record = self.db_handler.get_download_record_by_hash(file_hash)
        self.assertIsNotNone(record)
        self.assertEqual(record["filename"], "test_file.txt")

if __name__ == "__main__":
    unittest.main()