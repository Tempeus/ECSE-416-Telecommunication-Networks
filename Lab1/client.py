import socket
import sys
import time
import pickle

# ----------------- Default case for testing -----------------
HOST = '127.0.0.2'
PORT = 12345
timeout = 5
filename = "test.txt"

if(len(sys.argv) == 5):
    HOST = str(sys.argv[1])
    PORT = int(sys.argv[2])
    filename = str(sys.argv[3])
    timeout = int(sys.argv[4])

elif(len(sys.argv) == 4):
    HOST = str(sys.argv[1])
    PORT = int(sys.argv[2])
    filename = str(sys.argv[3])

else:
    print("Incorrect number of arguments")
    sys.exit(1)

# ----------------- Establishing Connection With Server -----------------
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

# ----------------- Formulating and Sending HTTP Request to Server -----------------
if filename.endswith(".txt"):
    request = "GET / HTTP/1.1\r\n Content-Type:text/html\n" + filename
elif filename.endswith(".jpg"):
    request = "GET / HTTP/1.1\r\n Content-Type:image/jpeg\n" + filename
else:
    print("file type not supported")
    sys.exit(1)

#Send file request message
clientsocket.send(request.encode())
print("Request Message Sent.")

# ----------------- Receive and Decode Response from Server -----------------
#Receive server response and content type
response = clientsocket.recv(1024)
print("Server HTTP Response:", response.decode('utf-8'))
if("404" in response.decode()):
	print("404 Not Found")
	clientsocket.close()
	sys.exit(1)

contenttype = clientsocket.recv(1024)
print("Content-Type:", contenttype.decode('utf-8'))

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

if(contenttype.decode() == "text/html"):
    print("Printing file content:")
    print(filecontent)

elif(contenttype.decode() == "image/jpg"):
    print("Showing Image:")
    filecontent.show()

clientsocket.close()
print("Socket Closed")
sys.exit(0)

#UTF-8 codec cant decode byte 0x80 in position 9: invalid start byte    
