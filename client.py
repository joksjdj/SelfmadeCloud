import socket
import zipfile
import os

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
    zip_ref.extractall("received_folder")

print("Folder extracted to ./received_folder")
