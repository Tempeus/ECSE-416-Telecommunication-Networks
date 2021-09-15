import socket

HOST = 'localhost'
PORT = 65432

#Creating a server socket
serversocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
#Bind the newly created socket to the localhost and specified port number
serversocket.bind((HOST, PORT))
print('set up server for', HOST, PORT)
#Listen for up to five connection requests
serversocket.listen(5)

#accept any connections
clientsocket, address = serversocket.accept()
with clientsocket:
    print('Connection established with:', address)
    while True:
        data = clientsocket.recv(1024)
        print('Request Message received.')
        if not data:
          print('Server HTTP Response: HTTP 404 Not Found')
          break;
        else:
          #parse the content of the data
          txt = str(data)
          print(txt)
          break;
serversocket.close()
