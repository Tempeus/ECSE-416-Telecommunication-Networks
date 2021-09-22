import socket
import pickle

HOST = 'localhost'
PORT = 65432

#Creating a server socket
serversocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
#Bind the newly created socket to the localhost and specified port number
serversocket.bind((HOST, PORT))
print('set up server for', HOST, PORT)
#Listen for up to five connection requests
serversocket.listen(1)

#Accept any connections
while True:
    clientsocket, address = serversocket.accept()
    with clientsocket:
        print('Connection established with:', address)
        filename = clientsocket.recv(4096).decode()
        print('Request Message received.')
        try:
            fext = filename.split(".")
            #if file is txt, content type is text/html
            if(fext[1] == 'txt'):
                data = open(filename, "r").read()
                contenttype = "text/html"
                filecontent = pickle.dumps(data)
            #if file is image, content type  is image/jpg
            elif(fext[1] == 'jpg'):
                data = open(filename, "r").read()
                contenttype = "image/jpg"
                filecontent = pickle.dumps(data)
            else:
                print("Invalid File Type")
                clientsocket.send("\HTTP/1.1 404 not found")
                print("Server Response Sent.")
                clientsocket.close()
                print("Socket closed and request cannot be completed")
                continue

        except IOError:
            print("Unknown file, must send failed message")
            resp = "\HTTP/1.1 404 not found"
            clientsocket.send(resp.encode())
            print("Server Response Sent.")
            clientsocket.close()
            print("Socket closed and request cannot be completed.")
            continue

    resp = "HTTP/1.1 200 OK"
    clientsocket.send(resp.encode())
    print("HTTP Response Sent.")
    #Send Content Type Response
    clientsocket.send(contenttype.encode())
    print("Content Type Response Sent.")
    #Send File Content Response
    clientsocket.send(filecontent)
    print("File Content Response Sent.")
    #Close Socket
    clientsocket.close()
    print("Socket closed and request completed.")
