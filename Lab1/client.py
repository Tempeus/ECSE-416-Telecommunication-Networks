import socket

HOST = 'localhost'
PORT = 65432
filename = 'test.txt'

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect((HOST, PORT))
print("Connection: OK")
fext = filename.split(".")
print(fext)

with open(filename, 'rb') as f:
    #send the type of file being sent to the server
    if fext[1] == "txt":
        s.send(b'TYPE txt')
    elif fext[1] == "jpg":    
        s.send(b'TYPE jpg')
    elif fext[1] == "mp4":
        s.send(b'TPYE mp4')
    elif fext[1] == "mp3":
        s.send(b'TPYE mp3')
    else:
        #Error?
        print('File type not supported')

    #Attempt to get confirmation from server that they received the file type and proceed to send the message
    if s.recv(4096) == 'RECV TYPE':
        print("Type confirmation received")   
        content = f.read()     
        s.send(content)
        print(content)
        print("Request message sent.")
        
        #When received message confirmation from server, send the EOT flag before closing the socket
        if s.recv(4096) == "RECV MSG":
            s.send("EOT")
            
s.close()
f.close()
