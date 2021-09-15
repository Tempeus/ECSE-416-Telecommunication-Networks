import socket

HOST = 'localhost'
PORT = 65432

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect((HOST, PORT))
s.sendall(b'Hello WORLD')
