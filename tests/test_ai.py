import unittest
import shutil
import os
from ai_duplicate_detection.model import AIDuplicateDetector

class TestAIModel(unittest.TestCase):
    def setUp(self):
        """
        Set up the test environment.
        """
        self.test_dir = "test_files"
        os.makedirs(self.test_dir, exist_ok=True)
        self.detector = AIDuplicateDetector()

    def tearDown(self):
        """
        Clean up the test environment.
        """
        shutil.rmtree(self.test_dir)

    def test_text_near_duplicate_detection(self):
        """
        Test near-duplicate detection for text files.
        """
        # Create two similar text files
        file1 = os.path.join(self.test_dir, "file1.txt")
        file2 = os.path.join(self.test_dir, "file2.txt")
        with open(file1, "w") as f:
            f.write("This is a test file.")
        with open(file2, "w") as f:
            f.write("This is a test file with minor changes.")

        # Detect near-duplicates
        duplicate = self.detector.detect_text_near_duplicate(file2, threshold=0.8)
        self.assertEqual(duplicate, file1)

    def test_image_near_duplicate_detection(self):
        """
        Test near-duplicate detection for image files.
        """
        # Create two similar image files (placeholder)
        file1 = os.path.join(self.test_dir, "image1.jpg")
        file2 = os.path.join(self.test_dir, "image2.jpg")
        with open(file1, "wb") as f:
            f.write(b"dummy image data")
        with open(file2, "wb") as f:
            f.write(b"dummy image data with minor changes")

        # Detect near-duplicates
        duplicate = self.detector.detect_image_near_duplicate(file2, hash_threshold=5, ssim_threshold=0.8)
        self.assertEqual(duplicate, file1)

if __name__ == "__main__":
    unittest.main()