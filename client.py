import socket

HOST = '100.99.236.89'  # sender's Tailscale IP
PORT = 5001

with socket.socket() as s:
    s.connect((HOST, PORT))
    with open("received.txt", "wb") as f:
        while True:
            data = s.recv(1024)
            if not data:
                break
            f.write(data)
print("File received.")