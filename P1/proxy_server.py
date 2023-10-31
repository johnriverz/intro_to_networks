'''
Juan Rios
CS 432: Intro to Networks

A simple HTTP Web Proxy Server that doesn't work
I think it's something wrong with my GET request or how I'm using makefile
'''

from socket import *
import sys
import traceback

if len(sys.argv) <= 1:
    print('Usage : "python ProxyServer.py server_ip"\n[server_ip : It is the IP Address Of Proxy Server')
    sys.exit(2)

SERVER = sys.argv[1]
PORT = 8102
ADDR = (SERVER, PORT)
DISCONNECT = '!DISCONNECT'
BUFSIZ = 4096

# Create a server socket, bind it to a port and start listening
tcpSerSock = socket(AF_INET, SOCK_STREAM)
try:
    # Fill in start.
    tcpSerSock.bind(ADDR)
    tcpSerSock.listen(5)
    # Fill in end.

    while True:
        # Start receiving data from the client
        print('Ready to serve...')
        tcpCliSock, addr = tcpSerSock.accept()

        print('Received a connection from:', addr)
        message = tcpCliSock.recv(BUFSIZ).decode() # FILL IN START FILL IN END
        print(message.split()[1])

        if '/favicon.ico' in message:
            continue

        print(message)

        # Extract the filename from the given message
        #print(message.split()[1])
        filename = message.split()[1].partition("/")[2]
        #print(filename)
        fileExist = False
        filetouse = "/" + filename
        #print(filetouse)

        try:
            # Check wether the file exist in the cache
            f = open(filetouse[1:], "r")
            outputdata = f.read()
            fileExist = "true"

            # ProxyServer finds a cache hit and generates a response message
            tcpCliSock.send("HTTP/1.0 200 OK\r\n".encode())
            tcpCliSock.send("Content-Type: text/html\r\n".encode())
            tcpCliSock.send("\r\n".encode())
            print("HTTP/1.0 200 OK\r\n")
            print("Content-Type: text/html\r\n")

            tcpCliSock.sendall(outputdata.encode())

            # tcpCliSock.close()
            f.close()

            print('Read from cache') 

        # Error handling for file not found in cache
        except IOError:
            if fileExist == False:
                # Create a socket on the proxyserver
                c = socket(AF_INET, SOCK_STREAM)
                hostn = filename.replace("www.","",1)
                #print(hostn)

                try:
                    # Connect to the socket to port 80
                    # Fill in start.
                    c.connect((filename, 80)) # initiates handshake
                    print("connecting...")
                    # Fill in end.

                    # # Create a temporary file on this socket and ask port 80 for the file requested by the client
                    fileobj = c.makefile('rwb', None)
                    fileobj.write(f'GET / Host: {hostn}'.encode())

                    # # Read the response into buffer
                    # # Fill in start.
                    buf = fileobj.read()
                    # # Fill in end.

                    # # # Create a new file in the cache for the requested file. 
                    # # # Also send the response in the buffer to client socket and the corresponding file in the cache
                    tmpFile = open("./" + filename,"wb") 

                    # Fill in start.
                    print(f'Caching...')
                    for i in range(len(buf)):
                        tmpFile.write(buf[i].encode())
                        tcpCliSock.send(buf[i].encode())
                        print(buf[i])
                    if tmpFile:
                        tmpFile.close()
                    if fileobj:
                        fileobj.close()
                    # Fill in end.

                except Exception as e:
                    print("Illegal request", e)
                    traceback.print_exc()
            else:
                # HTTP response message for file not found
                # Fill in start.
                print("fill in here")
                traceback.print_exc()
                # Fill in end.

        # Close the client and the server sockets 
        tcpCliSock.close() 
    # Fill in start.
    tcpSerSock.close()
    # Fill in end.  
except KeyboardInterrupt:
    print("SHUT IT DOWN")
    tcpSerSock.close()