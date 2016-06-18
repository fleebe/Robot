'''
Created on 7/06/2016

@author: phil
'''
from functools import partial
import socket  # Import socket module
import sys
from  _thread import start_new_thread
from usb_arm import Arm
import usb_arm
#from _dummy_thread import interrupt_main
from shared.mylogging import logging
from multiprocessing import Queue

#from usb_arm import usb_arm # @UnresolvedImport
# from _thread import start_new_thread
ARM_CONNECTED = False
#somewhere accessible to both:
key_queue = Queue()

class Arm2:
    
    def handle_key(self, arm, delay, key_map, key):
        def do_it():
            logging.debug("Handling key={}, delay={}".format(key, delay))
            if key in key_map:
                arm.move(key_map[key], delay)
        arm.safe_tell(do_it)

    def __init__(self):
        arm = Arm()
        km = usb_arm.make_keymap()
        self.handle = partial(self.handle_key, arm, 0.5, km)

    def processData(self, data):
#        dl = list(data)
        logging.debug('process Data...',data[0] )
        #       return
#        for d in dl:
        self.handle(data[0])

if __name__ == '__main__':                 
    #Function for handling connections. This will be used to create threads
    def clientthread(conn, arm):
        #infinite loop so that function do not terminate and thread do not end.
        while True:         
        #Receiving from client
            try:
                data = conn.recv(1024)
                reply = 'OK...' + data.decode()
                conn.sendall(reply.encode('utf-8'))
            except ConnectionResetError:
                logging.debug('Client exited')
                break
            
            logging.debug(reply)
            if not data: 
                logging.debug('Disconnected 1')
                key_queue.put('/')
                break
            if (data == '/'):
                logging.debug('Disconnected 2')
                key_queue.put(data)
                break
            #move the arm
            if (ARM_CONNECTED):
                arm.processData(data.decode())       
        #came out of loop
        logging.debug('Connection closed')
        conn.close()

    host = socket.gethostname() # Get local machine name
    port = 12345                # Reserve a port for your service.
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind((host, port))        # Bind to the port
        logging.debug('Binding {} : {}'.format(host,port))
        sock.listen(5)                 # Now wait for client connection.
        logging.debug('Socket now listening')
    except socket.error as msg:
        logging.debug('Error Code : {}  Message {}'.format(str(msg[0]), msg[1]))
        if (sock):
            sock.close()
        sys.exit()

# create arm processor object
    
    while True:
#wait to accept a connection - blocking call        
        c, addr = sock.accept()     # Establish connection with client.
        logging.debug('Got connection from {}'.format(addr))
        try:
            if (ARM_CONNECTED):
                arm = Arm2()
            c.sendall('Connected...'.encode())
        except AttributeError as e:
            err = "Please make sure the arm is connected and turned on"
            logging.debug(err)
            c.sendall(err.encode('utf-8'))
            break

    #start new thread takes 1st argument as a function name to be run, second is the tuple of arguments to the function.        
        try:
            if (ARM_CONNECTED):
                start_new_thread(clientthread ,(c,arm,))
            else:
                start_new_thread(clientthread ,(c,None,))
        finally:
            pass
# exit passed from client
        if (key_queue.get() == '/'):
            break;
        
    sock.close()
        