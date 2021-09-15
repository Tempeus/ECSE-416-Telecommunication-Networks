import socket

HOST = 'localhost'
PORT = 65432
filename = 'test.txt'

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect((HOST, PORT))
print("Connection: OK")
fext = filename.split(".")
print(fext)
if fext[1] == "txt":
    with open(filename, 'rb') as f:
        content = f.read()
        s.send(content)
        print(content)
elif fext[1] == "jpg":
    print("placeholder")
else:
    print("placeholder")
print("Request message sent.")

s.close()
