import os
import hashlib
import magic  # For file type detection

def extract_features(file_path):
    file_size = os.path.getsize(file_path)
    file_type = magic.from_file(file_path, mime=True)
    file_hash = hashlib.sha256(open(file_path, 'rb').read()).hexdigest()
    return {
        "size": file_size,
        "type": file_type,
        "hash": file_hash
    }
