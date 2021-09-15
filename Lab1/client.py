import socket

HOST = 'localhost'
PORT = 65432
filename = 'test.txt'

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect((HOST, PORT))
print("Connection: OK")
with open(filename, 'rb') as f:
    content = f.read()
    s.send(content)
    print(content)
print("Request message sent.")
