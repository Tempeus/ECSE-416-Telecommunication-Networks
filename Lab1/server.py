import socket
import pickle

HOST = '127.0.0.2'
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
        response = clientsocket.recv(1024).decode()
        temp = response.split("\n")
        filename = temp[2]

        print('Request Message received.')
        try:
            print(filename)
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
                clientsocket.sendall("\HTTP/1.1 404 not found")
                print("Server Response Sent.")
                clientsocket.close()
                print("Socket closed and request cannot be completed")
                continue

        except IOError:
            print("Unknown file, must send failed message")
            resp = "\HTTP/1.1 404 not found"
            clientsocket.sendall(resp.encode())
            print("Server Response Sent.")
            clientsocket.close()
            print("Socket closed and request cannot be completed.")
            continue

    resp = "HTTP/1.1 200 OK"
    clientsocket.sendall(resp.encode()) #Error Operation was attempted on something that is not a socket
    print("HTTP Response Sent.")

    #Send Content Type Response
    clientsocket.sendall(contenttype.encode())
    print("Content Type Response Sent.")
    
    #Send File Content Response
    clientsocket.sendall(filecontent)
    print("File Content Response Sent.")
    #Close Socket
    clientsocket.close()
    print("Socket closed and request completed.")
