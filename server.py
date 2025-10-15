import socket
import shutil
import os

HOST = ''  # listen on all interfaces
PORT = 5001
FOLDER_TO_SEND = "cloud"
ZIP_NAME = FOLDER_TO_SEND + ".zip"

# Step 1: Zip the folder
shutil.make_archive(FOLDER_TO_SEND, 'zip', FOLDER_TO_SEND)
file_size = os.path.getsize(ZIP_NAME)

# Step 2: Send over socket
with socket.socket() as s:
    s.bind((HOST, PORT))
    s.listen(1)
    print("Waiting for connection...")
    conn, addr = s.accept()
    print(f"Connected by {addr}")

    # Send file size first
    conn.sendall(str(file_size).encode() + b"\n")

    # Send the file
    with open(ZIP_NAME, "rb") as f:
        while True:
            data = f.read(4096)
            if not data:
                break
            conn.sendall(data)

    print("Folder sent as zip.")