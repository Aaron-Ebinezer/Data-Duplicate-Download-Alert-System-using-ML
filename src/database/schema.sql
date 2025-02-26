-- Table for storing download records
CREATE TABLE IF NOT EXISTS downloads (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    filename TEXT NOT NULL,
    file_hash TEXT NOT NULL,
    file_size INTEGER NOT NULL,
    mime_type TEXT NOT NULL,
    download_url TEXT NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Index for faster lookups by file hash
CREATE INDEX IF NOT EXISTS idx_file_hash ON downloads (file_hash);

-- Index for faster lookups by filename
CREATE INDEX IF NOT EXISTS idx_filename ON downloads (filename);