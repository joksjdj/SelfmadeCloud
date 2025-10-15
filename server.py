import socket
import shutil
import os
import threading

HOST = ''  # listen on all interfaces
PORT = 5001
FOLDER_TO_SEND = "Cloud_server"
ZIP_NAME = FOLDER_TO_SEND + ".zip"

# Step 0: Make sure folder exists
if not os.path.exists(FOLDER_TO_SEND):
    os.makedirs(FOLDER_TO_SEND)

def handle_client(conn, addr):
    print(f"Connected by {addr}")

    # Step 1: Zip the folder fresh for each connection
    shutil.make_archive(FOLDER_TO_SEND, 'zip', FOLDER_TO_SEND)
    file_size = os.path.getsize(ZIP_NAME)

    # Step 2: Send file size first
    conn.sendall(str(file_size).encode() + b"\n")

    # Step 3: Send the zip file
    with open(ZIP_NAME, "rb") as f:
        while True:
            data = f.read(4096)
            if not data:
                break
            conn.sendall(data)

    print(f"Folder sent to {addr}")

    # Optional: Delete zip after sending
    if os.path.exists(ZIP_NAME):
        os.remove(ZIP_NAME)

    conn.close()

# Main server loop
with socket.socket() as s:
    s.bind((HOST, PORT))
    s.listen()
    print(f"Server running on port {PORT}. Waiting for connections...")

    while True:
        conn, addr = s.accept()
        # Handle each client in a separate thread
        threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()
