import unittest
import shutil
import os
from antivirus_scan.scan import scan_file, quarantine_file, delete_file

class TestAntivirus(unittest.TestCase):
    def setUp(self):
        """
        Set up the test environment.
        """
        self.test_dir = "test_files"
        os.makedirs(self.test_dir, exist_ok=True)

    def tearDown(self):
        """
        Clean up the test environment.
        """
        shutil.rmtree(self.test_dir)

    def test_scan_file(self):
        """
        Test scanning a file for malware.
        """
        # Create a test file
        test_file = os.path.join(self.test_dir, "test_file.txt")
        with open(test_file, "w") as f:
            f.write("This is a test file.")

        # Scan the file
        result = scan_file(test_file)
        self.assertIn(result, ["clean", "infected", "error"])

    def test_quarantine_file(self):
        """
        Test quarantining an infected file.
        """
        # Create a test file
        test_file = os.path.join(self.test_dir, "test_file.txt")
        with open(test_file, "w") as f:
            f.write("This is a test file.")

        # Quarantine the file
        result = quarantine_file(test_file)
        self.assertTrue(result)

    def test_delete_file(self):
        """
        Test deleting an infected file.
        """
        # Create a test file
        test_file = os.path.join(self.test_dir, "test_file.txt")
        with open(test_file, "w") as f:
            f.write("This is a test file.")

        # Delete the file
        result = delete_file(test_file)
        self.assertTrue(result)

if __name__ == "__main__":
    unittest.main()