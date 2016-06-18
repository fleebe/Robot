"""Maplin USB Robot arm control.
Usage - 
>>> import usb_arm
>>> arm = usb_arm.Arm()
>>> arm.move(usb_arm.OpenGrips)
>>> arm.doActions(block_left) # WARNING - ARM SHOULD BE ALL THE WAY RIGHT BEFORE TRYING THIS

Trouble:
"NO back end found" - you need to install a libusb driver on your system.
"""
from time import sleep
import usb.core

class BitPattern(object):
    """A bit pattern to send to a robot arm"""
    __slots__ = ['arm', 'base', 'led']

    def __init__(self, arm, base, led):
        self.arm = arm
        self.base = base
        self.led = led

    def __iter__(self):
        return iter([self.arm, self.base, self.led])

    def __getitem__(self, item):
        return [self.arm, self.base, self.led][item]

    def __or__(self, other):
        return BitPattern(self.arm | other.arm,
                          self.base | other.base,
                          self.led | other.led)
    
    def __eq__(self, other):
        return self.arm == other.arm and self.base == other.base and self.led == other.led

    def __repr__(self):
        return "<BitPattern arm:%s base:%s led:%s>" % (self.arm, self.base, self.led)

    def __str__(self):
        return self.__repr__()    

GripsClose =       BitPattern(1, 0, 0)
GripsOpen =        BitPattern(2, 0, 0)
Stop =             BitPattern(0, 0, 0)
ElbowUp =          BitPattern(0x8, 0, 0)    
ElbowDown =        BitPattern(0x4, 0, 0)
WristUp =          BitPattern(0x20, 0, 0)
WristDown =        BitPattern(0x10, 0, 0)
ShoulderUp =       BitPattern(0x40, 0, 0)
ShoulderDown =     BitPattern(0x80, 0, 0)
BaseClockWise =    BitPattern(0, 1, 0)
BaseCtrClockWise = BitPattern(0, 2, 0)
LedOn =            BitPattern(0, 0, 1)
CloseGrips =       GripsClose
OpenGrips =        GripsOpen

def make_keymap():
    return {
            'z': BaseClockWise, 
            'x': BaseCtrClockWise,
            'r': CloseGrips,
            'f': OpenGrips,
            'a': ShoulderDown,
            'q': ShoulderUp,
            's': WristUp,   
            'w': WristDown, 
            'd': ElbowDown,  
            'e': ElbowUp,
            'l': LedOn,
            '.': Stop
    }



class Arm(object):
    """Arm interface"""
    __slots__ = ['dev']

    def __init__(self):
        self.dev = usb.core.find(idVendor=0x1267, idProduct=0x0)
        self.dev.set_configuration()

    def tell(self, msg):
        """Send a USB messaqe to the arm"""
        self.dev.ctrl_transfer(0x40, 6, 0x100, 0, msg)

    def safe_tell(self, fn):
        """Send a message to the arm, with a stop
        to ensure that the robot stops in the
        case of an exception"""
        try:
            fn()
        except:
            self.tell(Stop)
            raise

    def move(self, pattern, time=1):
        """Perform a pattern move with timing and stop"""
        try:
            self.tell(pattern)
            sleep(time)
        finally:
            self.tell(Stop)

    def doActions(self, actions):
        """Params: List of actions - each is a list/tuple of BitPattern and time
         (defaulting to 1 if not set)"""
        #Validate
        for action in actions:
            if not 1 <= len(action) <= 2:
                raise ValueError("Wrong number of parameters in action %s" %
                                 (repr(action)))
            if not isinstance(action[0], BitPattern):
                raise ValueError("Not a valid action")
        #Do
        try:
            for action in actions:
                if len(action) == 2:
                    time = action[1]
                else:
                    time = 1
                self.move(action[0], time)
        finally:
            self.move(self.bitpattern.Stop)

    def makeGrabAndMove(self, baseDir):
        return [[self.bitpattern.CloseGrips, 1.1],
                [self.bitpattern.ShoulderUp | self.bitpattern.ElbowUp | self.bitpattern.WristDown | baseDir],
                [baseDir, 8.5],
                [self.bitpattern.ShoulderDown | self.bitpattern.ElbowDown | self.bitpattern.WristUp | baseDir],
                [self.bitpattern.OpenGrips]]

# blink = [[LedOn, 0.5], [Stop, 0.5]] * 3
#block_left = makeGrabAndMove(BaseClockWise, 0.4) + blink
#block_right = makeGrabAndMove(BaseCtrClockWise, 0.4) + blink
