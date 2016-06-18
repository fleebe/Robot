'''
Created on Jun 11, 2016

@author: Phil
'''
import socket
from joystick2 import MyError

class RobotSocket(object):
    '''
    classdocs
    '''
    MSGLEN = 1024

    def get_constants(self, prefix):
    #Create a dictionary mapping socket module constants to their names.
        return dict( (getattr(socket, n), n)
                 for n in dir(socket)
                 if n.startswith(prefix)
                 )
        
    def __init__(self):
        '''
        Constructor
        '''
        self.skt = None
        try:
            host = socket.gethostname() # Get local machine name
 #           host = 'appalapachia' # Get local machine name
            port = 12345                # Reserve a port for your service.
            self.skt = socket.socket()         # Create a socket object

            families = self.get_constants('AF_')
            types = self.get_constants('SOCK_')
            protocols = self.get_constants('IPPROTO_')        
            print('Family  :', families[self.skt.family])
            print('Type    :', types[self.skt.type])
            print('Protocol:', protocols[self.skt.proto])
        
            self.skt.connect((host, port))
            msg = self.skt.recv(1024).decode()
            print(msg)
            if (msg != 'Connected...'):
                if self.skt:
                    self.skt.close()
                raise MyError(msg)
        except ConnectionRefusedError:
            if self.skt:
                self.skt.close()
            print('Connection refused')
            raise
            
        except socket.timeout as err:
            if self.skt:
                self.skt.close()
            print('Timeout {} : {}'.format([host,port]))
            
        except socket.gaierror:
        #could not resolve
            if self.skt:
                self.skt.close()
            print('Hostname could not be resolved. Exiting Host {} : {}'.format([host,port]))
    
        except socket.error as err:
            print('Socket connect failed. Error Code : {}  Message {}'.format(str(err[0]), err[1]))
            if self.skt:
                self.skt.close()        
        except OSError as err:
            if self.skt:
                self.skt.close()
            print("OSError")
                        
 #       finally:
 #           return self.skt


    def send(self, key):
        try:
            if (self.skt is None):
                print('skt is none')
#test send receive from/to client/server        
#            msg = 'Joystick command'
#            skt.send(msg.encode('utf-8'))
#            msg = skt.recv(1024)
#            print(msg.decode())
            # key pressed or calculated so send
            if (not key is None):
#                print(key)
                self.skt.send(key.encode('utf-8'))
                # gets data from the server
                msg = self.skt.recv(1024)
                print(msg.decode())
        except socket.error as err: 
            print('Send failed :{}'.format(err))

    def close(self):
        if (self.skt):    
            self.skt.close()

    def __del__(self):
        self.close()

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
    
    def mysend(self, msg):
        totalsent = 0
        while totalsent < self.MSGLEN:
            sent = self.sock.send(msg[totalsent:])
            if sent == 0:
                raise RuntimeError("socket connection broken")
            totalsent = totalsent + sent