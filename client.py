import socket
import zipfile
import time
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

HOST = '100.99.236.89'  # sender's Tailscale IP
PORT = 5001
OUTPUT_ZIP = "received_folder.zip"

with socket.socket() as s:
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

print("File received. Extracting...")

# Unzip the folder
with zipfile.ZipFile(OUTPUT_ZIP, 'r') as zip_ref:
    zip_ref.extractall("Cloud")
    
if os.path.exists(OUTPUT_ZIP):
    os.remove(OUTPUT_ZIP)
    print(f"Deleted file: {OUTPUT_ZIP}")
else:
    print("File not found.")

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
