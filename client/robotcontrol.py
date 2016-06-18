'''
Created on Jun 12, 2016

@author: Phil
'''
import pygame
from eventwindow import EventWindow
from joystick2 import Joystick, MyError
from robotsocket import RobotSocket
import time
#from camera import Capture
from shared.mylogging import logging

class RobotControl(object):
    '''
    classdocs
    '''
    def __init__(self):
        '''
        Constructor
        '''
        pygame.init()
        self.clock = pygame.time.Clock()
# When to send a new action to the server for axis moves.
        self.DELAY = 0.5
        self.currTime = time.clock()
        self.curKey = None
        self.skt = None
        self.key = None 
        pygame.event.set_blocked([pygame.HAT_DOWN, pygame.HAT_UP])
        pygame.event.set_allowed([pygame.JOYBUTTONDOWN, pygame.JOYAXISMOTION, pygame.JOYHATMOTION, pygame.KEYDOWN ])
        try:
            self.ew = EventWindow()
#            self.camera = Capture()
            self.joystick = Joystick()
            
        except MyError as e: 
            logging.debug('Myerror: {}'.format(e.value))
#           pygame.quit()
#           sys.exit()
    # Used to manage how fast the screen updates   
    '''
    '''
    def createRemote(self):
        try:
            self.skt = RobotSocket()
        except ConnectionRefusedError:
            if self.skt:
                self.skt.close()

    def __del__(self):
        if self.skt:
            self.skt.close()
        pygame.quit()
    '''
    '''
    def newSend(self, key):
        diff = time.clock() - self.currTime
        if (self.key == self.curKey):
            if (diff > self.DELAY):
                self.skt.send(key)
                self.curKey = key
                self.key = None
                self.currTime = time.clock()
        else:
            self.skt.send(key)
            self.curKey = key
            self.key = None
            self.currTime = time.clock()
            
    '''
    '''
    def eventLoop(self):
    #Loop until the user clicks the close button.
        done = False
        while done==False:
            # EVENT PROCESSING STEP in pygame window
            event = pygame.event.wait()
            et = event.type
            self.key = None 
#            logging.debug(event)
    #        event = pygame.event.poll()
    #        for et in pygame.event.get(): # User did something
            
            if et == pygame.QUIT: # If user clicked close
                done=True # Flag that we are done so we exit this loop       
            # Possible joystick actions: JOYAXISMOTION JOYBALLMOTION JOYBUTTONDOWN JOYBUTTONUP JOYHATMOTION
            elif et == pygame.JOYBUTTONDOWN:
                logging.debug("JOYBUTTONDOWN")
                self.joystick.buttonChange()
            elif et == pygame.JOYBUTTONUP:
                pass
#                logging.debug("JOYBUTTONUP")
#                self.joystick.buttonChange()
            elif et == pygame.JOYAXISMOTION:
#gets lots of signals from axis 2 throttle
#                logging.debug("JOYAXISMOTION")
                self.key = self.joystick.axisChange()
                self.newSend(self.key)
            elif et == pygame.JOYBALLMOTION:
                logging.debug("JOYBALLMOTION")
            elif et == pygame.MOUSEBUTTONDOWN:
                logging.debug("MOUSEBUTTONDOWN")
            elif et == pygame.JOYHATMOTION:
                logging.debug("JOYHATMOTION")
                self.key = self.joystick.hatChange()
                self.newSend(self.key)
            elif et == pygame.KEYDOWN:
                self.key = pygame.key.name(event.key)
                logging.debug("KEYDOWN {}".format(self.key))
                self.newSend(self.key)
                if event.key == ord('/'):
                    done = True
                                      
            pygame.event.clear()
        # Limit to 20 frames per second
            #sleep(1000)
            self.clock.tick(5)
            
        # Close the window and quit.
        # If you forget this line, the program will 'hang'
        # on exit if running from IDLE.
        pygame.joystick.quit()
        pygame.quit ()
        if (self.skt):    
            self.skt.close()
