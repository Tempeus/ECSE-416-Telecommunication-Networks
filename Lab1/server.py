import socket

HOST = 'localhost'
PORT = 65432
newname = "image%s.png"

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
        data = clientsocket.recv(4096)
        print('Request Message received.')
        if not data:
            print('Server HTTP Response: HTTP 404 Not Found')
            break
        else:
            #parse the content of the data
            txt = str(data)
            filetype = ''
            print(txt)
            
            #receive message type and send receive confirmation
            if txt.startswith('TYPE'):
                tmp = txt.split()
                filetype = tmp[1]
                serversocket.send(b"RECV TYPE")

            #receive if it is EOT
            elif txt.startswith('EOT'):
                serversocket.close()
                
            #read the message    
            elif data:
                if filetype == "txt":
                    print(data)

                elif filetype == "png":
                    recvimg = open(newname, 'wb')
                    data = serversocket.recv(4096000)
                    if not data:
                        recvimg.close()
                        print("404?")
                        break
                    recvimg.write(data)
                    recvimg.close()

                    print("Message received.")
                    serversocket.send(b"RECV MSG")
                    serversocket.close()
        break

serversocket.close()
