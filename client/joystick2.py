'''
Created on Jun 8, 2016

@author: Phil
'''

from collections import namedtuple
from shared.mylogging import logging

import pygame


class MyError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)


class Joystick:
 
    buttonType = namedtuple('ButtonMap', ['num', 'onoff', 'name', 'KeyboardKey'])
    buttonTuple = (
        buttonType(0,1,'',''),
        buttonType(1,1,'',''),
        buttonType(2,1,'',''),
        buttonType(3,1,'',''),
        buttonType(4,1,'',''),
        buttonType(5,1,'',''),
        buttonType(6,1,'',''),
        buttonType(7,1,'',''),
        buttonType(8,1,'',''),
        buttonType(9,1,'',''),
        buttonType(10,1,'',''),
        buttonType(11,1,'','')
        )
     
    joyTuple = namedtuple('JoystickMap',
        ['num1','num2', 'JoystickDirection', 'KeyboardKey','ArmMovement'])
    
    axes_idx = ((0,1),(0,-1),(1,-1),(1,1),(2,1),(2,-1),(3,1),(3,-1),(0,0))
    axesTuple = (
        joyTuple(0,1,'Right','d','ElbowDown'),
        joyTuple(0,-1,'left','e','ElbowUp'),
        joyTuple(1,-1,'Forward','a','ShoulderDown'),
        joyTuple(1,1, 'Backward','q','ShoulderUp'),
        joyTuple(2,1,'ThrottleDown','',''),
        joyTuple(2,-1,'ThrottleUp','',''),
        joyTuple(3,1,'RotateRight','z','BaseClockwise'),
        joyTuple(3,-1,'RotateLeft','x','BaseCtrClockwise'),
        joyTuple(0,0,'Centre','.','Stop'))
    
    hat_idx = ((0,1),(0,-1),(1,0),(-1,0))
    hatTuple = (
        joyTuple(0,1,'Hat Forward','r','CloseGrip'),
        joyTuple(0,-1,'Hat Back','f','OepnGrip'),
        joyTuple(1,0,'Hat Right','s','WristUp'),
        joyTuple(-1,0,'Hat Left','w','wristDown'))
            
    def __init__(self):
        pygame.joystick.init()
    # Initialize the joysticks
        if pygame.joystick.get_init():
            logging.debug('joystick init')

        joystick_count = pygame.joystick.get_count()
        if joystick_count != 1:
    #        logging.debug('Please connect a single joystick')
            raise MyError('Please connect a single joystick cnt {}'.format(joystick_count))
    
        # For each joystick:
        #for i in range(joystick_count):
        #    joystick = pygame.joystick.Joystick(i)
        #    logging.debug(joystick.get_name())
        
        # exit()              
#hat_km_idx = (pygame.HAT_UP,pygame.HAT_DOWN,pygame.HAT_RIGHT,pygame.HAT_LEFT)  

        for at in self.axesTuple:
            logging.debug(at)
        logging.debug('------------------')
        '''
        for i,h in zip(hat_km_idx, hatTuple):
            if (i == pygame.HAT_UP):
                logging.debug(h)
        ''' 
                
        self.joystick = pygame.joystick.Joystick(0)
        self.joystick.init()
        
        # Get the name from the OS for the controller/joystick
        name = self.joystick.get_name()
        logging.debug("Joystick name: {}".format(name) )
        
        # Usually axis run in pairs, up/down for one, and left/right for
        # the other.
        self.axes = list(0 for i in range(self.joystick.get_numaxes()))
        logging.debug("Number of axes: {}".format(len(self.axes)) )
                    
        self.buttons = list(0 for i in range(self.joystick.get_numbuttons()))
        logging.debug("Number of buttons: {}".format(len(self.buttons)) )
                    
        # Hat switch. All or nothing for direction, not like joysticks.
        # Value comes back in an array.
        self.hats = list(0 for i in range(self.joystick.get_numhats()))
        logging.debug("Number of hats: {}".format(len(self.hats)) )
         
    def __del__(self):
        pygame.joystick.quit()

    def buttonChange(self):
        key = None 
        for i in range( len(self.buttons) ):
            button = self.joystick.get_button( i )
            if (button):
                logging.debug("Button {:>2} value: {}".format(i,button) )
    
    def hatChange(self):
        key = None
        for i in range( len(self.hats) ):
            hat = self.joystick.get_hat( i )
            for s in self.hat_idx:
                if (hat == s):
                    j = self.hat_idx.index(s, )
                    logging.debug("Hat {} Idx {} value: {}".format(i, j, str(hat)) )
                    logging.debug(self.hatTuple[j])
                    key = self.hatTuple[j].KeyboardKey
 #                   logging.debug("Key={}".format(key))
                    break
        return key

        
    def axisChange(self):
        key = None
        for i in range( len(self.axes) ):
            # detects the axis 0..3
            if (i == 2):
            # throttle
                continue
        # gets the position
            axis_pos = self.joystick.get_axis( i )
            if (abs(axis_pos) > 0.5):
                if (axis_pos < 0): j = -1 
                else: j = 1
                #get the index of the axis moved.
                k = self.axes_idx.index((i,j), )            
                logging.debug(self.axesTuple[k])
                key = self.axesTuple[k].KeyboardKey
  #              logging.debug("Key={}".format(key))
                
                if (j == 1):
                    logging.debug("Axis {} value: {:>6.3f}".format(i, axis_pos) )
                elif (j == -1):
                    logging.debug("Axis {} value: {:>6.3f}".format(i, axis_pos) )
            else:
                #centered
                k = self.axes_idx.index((0,0), )            
                logging.debug(self.axesTuple[k])
                key = self.axesTuple[k].KeyboardKey
                pass
        return key