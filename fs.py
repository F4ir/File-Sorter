# File-Storage was proudly coded by F4ir

import os
import time
import shutil
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Define the folder to be monitored
DOWNLOADS_FOLDER = os.path.expanduser("~/Downloads")

# Define target folders for each file type
TARGET_FOLDERS = {
    "executables": os.path.join(DOWNLOADS_FOLDER, "Executables"),
    "compressed": os.path.join(DOWNLOADS_FOLDER, "Compressed"),
    "images": os.path.join(DOWNLOADS_FOLDER, "Images"),
    "audio": os.path.join(DOWNLOADS_FOLDER, "Audio"),
    "video": os.path.join(DOWNLOADS_FOLDER, "Video"),
    "documents": os.path.join(DOWNLOADS_FOLDER, "Documents"),
    "others": os.path.join(DOWNLOADS_FOLDER, "Others")
}

# Define file extensions for each category
EXTENSIONS = {
    "executables": [".exe", ".msi"],
    "images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff"],
    "audio": [".mp3", ".wav", ".aac", ".flac", ".ogg"],
    "video": [".mp4", ".mkv", ".avi", ".mov", ".wmv", ".flv"],
    "documents": [".pdf", ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx", ".txt"],
    "compressed": [".zip", ".tgz", ".rar", ".rar4"]
}

# Create target folders if they don't exist
for folder in TARGET_FOLDERS.values():
    os.makedirs(folder, exist_ok=True)

class FileHandler(FileSystemEventHandler):
    def on_modified(self, event):
        self.organize_files()

    def is_file_complete(self, file_path):
        """Check if the file is still being downloaded."""
        return not (file_path.endswith('.part') or file_path.endswith('.opdownload') or file_path.endswith('.tmp'))

    def organize_files(self):
        for filename in os.listdir(DOWNLOADS_FOLDER):
            src_path = os.path.join(DOWNLOADS_FOLDER, filename)

            if os.path.isfile(src_path) and self.is_file_complete(src_path):
                self.move_file(src_path)

    def move_file(self, src_path):
        _, ext = os.path.splitext(src_path)
        ext = ext.lower()

        for category, extensions in EXTENSIONS.items():
            if ext in extensions:
                target_folder = TARGET_FOLDERS[category]
                break
        else:
            target_folder = TARGET_FOLDERS["others"]

        # Move file if it's not already in the target folder
        target_path = os.path.join(target_folder, os.path.basename(src_path))
        if not os.path.exists(target_path):
            shutil.move(src_path, target_path)

if __name__ == "__main__":
    # Organize existing files on startup
    handler = FileHandler()
    handler.organize_files()

    # Set up the observer for new files
    observer = Observer()
    observer.schedule(handler, DOWNLOADS_FOLDER, recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

# File-Storage was proudly coded by F4ir
