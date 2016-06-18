'''
Created on 10/06/2016

@author: phil
'''
import socket

class Connect(object):

    def connect(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print('connecting to host')
        host = socket.gethostname() # Get local machine name
        port = 12345                # Reserve a port for your service.        
        try:
            sock.bind((host, port))        # Bind to the port
            print('Listening ', host, ':', port)
        except socket.error as msg:
            print('Bind failed. Error Code : {}  Message {}'.format(str(msg[0]), msg[1]))
            exit(1)
        print('Socket bind complete')              
        sock.listen(5)                 # Now wait for client connection.
        print('Socket now listening')
        return sock

    def send(self, command):
        sock = self.connect()
        recv_data = ""
        data = True

        print('sending: ' + command)
        sock.sendall(command)

        while data:
            data = sock.recv(1024)
            recv_data += data 
            print('received: ' + data)

        sock.close()
        return recv_data