# i) create a connection socket when contacted by a client
# (browser);
# (ii) receive the HTTP request from this connection;
# (iii) parse the request to determine the
# specific file being requested;
# (iv) get the requested file from the server’s file system;
# (v) create an HTTP
# response message consisting of the requested file preceded by header lines;
# (vi) send the response over the TCP connection to the requesting browser. If a browser requests a file that is not present in your server,
# your server should return a “404 Not Found” error message.

import sys
#import socket module
from socket import *
from dotenv import load_dotenv
import os

load_dotenv()

def main():
    serverSocket = socket(AF_INET, SOCK_STREAM)

    #Prepare a sever socket
    host, port = os.environ.get('host'), int(os.environ.get('port'))
    serverSocket.bind((host, port))
    serverSocket.listen(1)

    while True:
        #Establish the connection
        print('Ready to serve...')
        connectionSocket, addr = serverSocket.accept()
        try:
            message = connectionSocket.recv(1024).decode()
            filename = message.split()[1]
            f = open(filename[1:])
            outputdata = f.read()
            f.close()
            #Send one HTTP header line into socket
            connectionSocket.send('HTTP/1.0 200 OK\nContent-Type: text/html\n\n'.encode())
            #Send the content of the requested file to the client
            for i in range(len(outputdata)):
                connectionSocket.send(outputdata[i].encode())
            connectionSocket.send("\r\n".encode())

        except IOError as e:
            #Send response message for file not found
            errorMessage = 'File could not be found'
            connectionSocket.send(errorMessage.encode())
        finally:
            # Close client socket
            connectionSocket.close()

    serverSocket.close()
    sys.exit()#Terminate the program after sending the corresponding data


main()
