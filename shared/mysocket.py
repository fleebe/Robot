'''
Created on 9/06/2016

@author: phil
'''
import socket


class MySocket:
    """demonstration class only
      - coded for clarity, not efficiency
    """
    MSGLEN = 1024

    def __init__(self, sock=None):
        if sock is None:
            self.sock = socket.socket(
                            socket.AF_INET, socket.SOCK_STREAM)
        else:
            self.sock = sock

    def connect(self, host, port):
#            self.sock.connect((host, port))
        self.sock.bind((host, port))        # Bind to the port
        print('Binding ', host, ':', port)
        self.sock.listen(5)                 # Now wait for client connection.
        print('Socket now listening')
           
    def mysend(self, msg):
        totalsent = 0
        while totalsent < self.MSGLEN:
            sent = self.sock.send(msg[totalsent:])
            if sent == 0:
                raise RuntimeError("socket connection broken")
            totalsent = totalsent + sent

    def accept(self):
        return self.sock.accept()
    
    def close(self):
        print('Closing mysocket')
        self.sock.close()
    
    def myreceive(self):
        chunks = []
        bytes_recd = 0
        while bytes_recd < self.MSGLEN:
            chunk = self.sock.recv(min(self.MSGLEN - bytes_recd, 2048))
            if chunk == b'':
                raise RuntimeError("socket connection broken")
            chunks.append(chunk)
            bytes_recd = bytes_recd + len(chunk)
        return b''.join(chunks)