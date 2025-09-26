#!/usr/bin/python3

import socket
import sys

def main(argv):
    # get port number from argv
    port = int(argv[1])
   
    # create socket and bind
    sockfd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        sockfd.bind(("", port))
    except socket.error as err:
        print("Socket bind error: ", err)

    sockfd.listen(5)
    
    print("The server is ready to receive")
    
    while True:
        
        # accept new connection
        try:
            conn, address = sockfd.accept()
        except socket.error as err:
            print("Socket accept error: ", err)
        
        # receive file name/size message from client 
        try:
            message = conn.recv(1024)
        except socket.error as err:
            print("Recv error: ", err)
        
        #use Python string split function to retrieve file name and file size from the received message
        fname, filesize = message.decode('ascii').rsplit(':', 1)
        
        print("Open a file with name \'%s\' with size %s bytes" % (fname, filesize))
        
        #create a new file with fname
        try:
            fd = open(fname, 'ab')
        except OSError as err:
            print('Failed to open file: ', err)
        
        remaining = int(filesize)

        conn.send(b"OK")

        print("Start receiving . . .")
        while remaining > 0:
            # receive the file content into rmsg and write into the file
            
            try:
                rmsg = conn.recv(1000)
                fd.write(rmsg)
            except socket.error as err:
                print("Recv error: ", err)
            except OSError as err:
                print("OS error: ", err)

            
            remaining -= len(rmsg)

        print("[Completed]")
        fd.close()
        conn.close()
        
    sockfd.close()
    

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python3 FTServer.py <Server_port>")
        sys.exit(1)
    main(sys.argv)