HOST = '172.16.0.183'
PORT = 2222
#MI INTERESSA GLLL --- prima lat poi long
import socket

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    #s.sendall(b"Hello, world")
    data = s.recv(1024)

print(f"Received {data!r}")