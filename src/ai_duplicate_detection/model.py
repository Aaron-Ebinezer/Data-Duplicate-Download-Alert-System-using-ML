import os
import numpy as np
from PIL import Image
import imagehash
from skimage.metrics import structural_similarity as ssim
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from logger import setup_logger

# Initialize logging
logger = setup_logger()

class AIDuplicateDetector:
    def __init__(self):
        """
        Initialize the AI duplicate detector.
        """
        self.vectorizer = TfidfVectorizer()  # For text similarity
        self.file_contents = {}  # Stores file contents for text files
        self.image_hashes = {}  # Stores perceptual hashes for images

    def load_file_content(self, file_path):
        """
        Load the content of a text file.

        Args:
            file_path (str): Path to the file.

        Returns:
            str: Content of the file.
        """
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return f.read()
        except Exception as e:
            logger.error(f"Error reading file {file_path}: {e}")
            return None

    def detect_text_near_duplicate(self, file_path, threshold=0.8):
        """
        Detect near-duplicates in text files using cosine similarity on TF-IDF vectors.

        Args:
            file_path (str): Path to the file.
            threshold (float): Similarity threshold (0 to 1).

        Returns:
            str: Path to the near-duplicate file if found, otherwise None.
        """
        content = self.load_file_content(file_path)
        if not content:
            return None

        # Update TF-IDF vectors
        self.file_contents[file_path] = content
        texts = list(self.file_contents.values())
        tfidf_matrix = self.vectorizer.fit_transform(texts)

        # Compare the new file with existing files
        new_file_index = list(self.file_contents.keys()).index(file_path)
        similarities = cosine_similarity(tfidf_matrix[new_file_index], tfidf_matrix)

        for i, sim in enumerate(similarities[0]):
            if i != new_file_index and sim >= threshold:
                duplicate_file = list(self.file_contents.keys())[i]
                logger.info(f"Near-duplicate text file found: {duplicate_file} (similarity: {sim:.2f})")
                return duplicate_file

        return None

    def calculate_image_hash(self, file_path):
        """
        Calculate the perceptual hash (pHash) of an image.

        Args:
            file_path (str): Path to the image file.

        Returns:
            imagehash.ImageHash: Perceptual hash of the image.
        """
        try:
            with Image.open(file_path) as img:
                return imagehash.phash(img)
        except Exception as e:
            logger.error(f"Error calculating hash for image {file_path}: {e}")
            return None

    def calculate_ssim(self, img1_path, img2_path):
        """
        Calculate the Structural Similarity Index (SSIM) between two images.

        Args:
            img1_path (str): Path to the first image.
            img2_path (str): Path to the second image.

        Returns:
            float: SSIM score (0 to 1).
        """
        try:
            img1 = np.array(Image.open(img1_path).convert("L"))
            img2 = np.array(Image.open(img2_path).convert("L"))
            return ssim(img1, img2)
        except Exception as e:
            logger.error(f"Error calculating SSIM for {img1_path} and {img2_path}: {e}")
            return 0.0

    def detect_image_near_duplicate(self, file_path, hash_threshold=5, ssim_threshold=0.8):
        """
        Detect near-duplicates in images using perceptual hashing and SSIM.

        Args:
            file_path (str): Path to the image file.
            hash_threshold (int): Maximum hash difference for near-duplicates.
            ssim_threshold (float): Minimum SSIM score for near-duplicates.

        Returns:
            str: Path to the near-duplicate image if found, otherwise None.
        """
        img_hash = self.calculate_image_hash(file_path)
        if not img_hash:
            return None

        # Compare with existing image hashes
        for existing_file, existing_hash in self.image_hashes.items():
            hash_diff = img_hash - existing_hash
            if hash_diff <= hash_threshold:
                # Verify with SSIM for higher accuracy
                ssim_score = self.calculate_ssim(file_path, existing_file)
                if ssim_score >= ssim_threshold:
                    logger.info(f"Near-duplicate image found: {existing_file} (SSIM: {ssim_score:.2f})")
                    return existing_file

        # Add the new image hash to the database
        self.image_hashes[file_path] = img_hash
        return None