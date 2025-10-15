import socket

HOST = ''  # listen on all interfaces
PORT = 5001

with socket.socket() as s:
    s.bind((HOST, PORT))
    s.listen(1)
    print("Waiting for connection...")
    conn, addr = s.accept()
    print(f"Connected by {addr}")
    with conn, open("file_to_send.txt", "rb") as f:
        data = f.read(1024)
        while data:
            conn.sendall(data)
            data = f.read(1024)
    print("File sent.")