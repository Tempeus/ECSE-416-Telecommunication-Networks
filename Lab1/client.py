import socket
import sys
import time
import pickle

HOST = 'localhost'
PORT = 65432
timeout = 5

filename = 'text.txt'
#Create a client socket to send requests and receives message data
clientsocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
#set the timeout
clientsocket.settimeout(timeout)
try:
    clientsocket.connect((HOST, PORT))
except socket.error:
    print("Connection: Not Okay")
    sys.exit(1)
print("Connection: OK")

#Send file request message
clientsocket.send(filename.encode())
print("Request Message Sent")

#Receive server response and content type
response = clientsocket.recv(4096).decode()
print("Server HTTP Response:", response)
contenttype = clientsocket.recv(4096).decode()
print("Content-Type:", contenttype)

#Begin receiving the data
datarecv = []
starttime = time.time()
numpack = 0
while True:
    packet = clientsocket.recv(1024)
    if not packet:
        break
    datarecv.append(packet)
    numpack += 1

filecontent = pickle.loads(b"".join(datarecv))

print("Time elapsed:", (time.time() - starttime))
print("Number of packets:", numpack)

if(contenttype == "text/html"):
    print(filecontent)
elif(contenttype == "image/jpg"):
    filecontent.show()

clientsocket.close()
print("Socket Closed")
sys.exit(0)

clientsocket.close()
