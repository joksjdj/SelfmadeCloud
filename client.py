import socket
import zipfile
import time
import os
import hashlib
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

HOST = '100.99.236.89'  # sender's Tailscale IP
PORT = 5001
OUTPUT_ZIP = "received_folder.zip"

s = socket.socket()
s.connect((HOST, PORT))

# Receive the file size first
file_size = int(s.recv(1024).decode().strip())
print(f"Receiving {file_size} bytes...")

# Receive the zip file
received = 0
with open(OUTPUT_ZIP, "wb") as f:
    while received < file_size:
        data = s.recv(4096)
        if not data:
            break
        f.write(data)
        received += len(data)


# =================================================================

ZIP_FILE = "received_folder.zip"
FOLDER = "Cloud"
# Function to compute hash of a normal file
# Function to compute hash of a normal file
def file_hash(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            h.update(chunk)
    return h.hexdigest()

# Function to compute hash of a file inside a ZIP
def zip_file_hash(zip_ref, name):
    h = hashlib.sha256()
    with zip_ref.open(name) as f:
        for chunk in iter(lambda: f.read(4096), b""):
            h.update(chunk)
    return h.hexdigest()

# Function to extract a file from ZIP to folder
def extract_file(zip_ref, name, folder_path):
    dest_path = os.path.join(FOLDER, name.replace("/", os.sep))
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with zip_ref.open(name) as src, open(dest_path, "wb") as dst:
        for chunk in iter(lambda: src.read(4096), b""):
            dst.write(chunk)
    print(f"✅ Updated: {name}")

# =======================
# Sync folder with ZIP
# =======================
with zipfile.ZipFile(ZIP_FILE, 'r') as zip_ref:
    zip_files = zip_ref.namelist()

    # Replace missing or different files
    for name in zip_files:
        folder_path = os.path.join(FOLDER, name.replace("/", os.sep))
        replace = False

        if os.path.exists(folder_path):
            zip_h = zip_file_hash(zip_ref, name)
            folder_h = file_hash(folder_path)
            if zip_h != folder_h:
                replace = True
        else:
            replace = True

        if replace:
            extract_file(zip_ref, name, folder_path)

print("✅ Folder synchronized with ZIP.")

if os.path.exists(OUTPUT_ZIP):
    os.remove(OUTPUT_ZIP)
    print(f"Deleted file: {OUTPUT_ZIP}")
else:
    print("File not found.")

# ==================================================================

FOLDER_TO_WATCH = "Cloud"

class MyHandler(FileSystemEventHandler):
    def on_created(self, event):
        print(f"Created: {event.src_path}")

    def on_deleted(self, event):
        print(f"Deleted: {event.src_path}")

    def on_modified(self, event):
        if not event.is_directory:
            print(f"Modified: {event.src_path}")

    def on_moved(self, event):
        print(f"Moved: {event.src_path} → {event.dest_path}")

if __name__ == "__main__":
    observer = Observer()
    observer.schedule(MyHandler(), FOLDER_TO_WATCH, recursive=True)
    observer.start()
    print(f"Watching folder: {os.path.abspath(FOLDER_TO_WATCH)}")

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    observer.stop()
observer.join()

print("Folder extracted to ./received_folder")
