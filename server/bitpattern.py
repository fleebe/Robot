


class ArmAction(object):
#   def __init__(self):

    def make_keymap(self):
        return {
                'z': self.BaseClockWise, 
                'x': self.BaseCtrClockWise,
                'r': self.CloseGrips,
                'f': self.OpenGrips,
                'a': self.ShoulderDown,
                'q': self.ShoulderUp,
                's': self.WristUp,   
                'w': self.WristDown, 
                'd': self.ElbowDown,  
                'e': self.ElbowUp,
                'l': self.LedOn,
                '.': self.Stop
        }
