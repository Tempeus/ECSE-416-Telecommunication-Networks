import socket
import sys
import time
import pickle

#Default case for testing
HOST = '127.0.0.2'
PORT = 65432
timeout = 5
filename = "text.txt"

if(len(sys.argv) == 5):
    HOST = str(sys.argv[1])
    PORT = int(sys.argv[2])
    filename = str(sys.argv[3])
    timeout = int(sys.argv[4])

elif(len(sys.argv) == 4):
    HOST = str(sys.argv[1])
    PORT = int(sys.argv[2])
    filename = str(sys.argv[3])

#else:
#    print("Incorrect number of arguments")
#    sys.exit(1)

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

request = "GET / HTTP/1.1\r\n Content-Type:text/html\n" + filename

#Send file request message
clientsocket.send(request.encode())
print("Request Message Sent")

#Receive server response and content type
response = clientsocket.recv(1024)
print("Server HTTP Response:", response.decode())
contenttype = clientsocket.recv(1024).decode("utf-8")
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
