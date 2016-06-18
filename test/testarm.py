'''
Created on Jun 12, 2016

@author: Phil
'''
import unittest
from joystick2 import Joystick
import pygame
from robotcontrol import RobotControl
from camera import Capture

class TestCamera(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)
        pygame.init()
        self.camera = Capture()
        
    def tearDown(self):
        pygame.quit()
        unittest.TestCase.tearDown(self)
        
    def test_Camera(self):
        pass



class TestJoystick(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)
        pygame.init()
        self.rc = RobotControl()
        self.rc.eventLoop()
        
    def tearDown(self):
        pygame.quit()
        unittest.TestCase.tearDown(self)
        
    def test_Signal(self):
        pygame.event.post(pygame.JOYBUTTONUP)
        pass


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
#    suite = unittest.TestLoader().loadTestsFromTestCase(TestJoystick)
    suite = unittest.TestLoader().loadTestsFromTestCase(TestCamera)
    unittest.TextTestRunner(verbosity=2).run(suite)
#    unittest.main()