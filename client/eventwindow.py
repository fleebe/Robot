'''
Created on 8/06/2016

@author: phil
'''
import pygame


class EventWindow(object):
    # Define some colors
    BLACK    = (   0,   0,   0)
    WHITE    = ( 255, 255, 255)
        
#    pygame.init()
    def __init__(self):
        pygame.display.init()
# Set the width and height of the screen [width,height]
        size = [200, 200]
        screen = pygame.display.set_mode(size)
        screen.fill(self.WHITE)

        pygame.display.set_caption("My Game")
        
    def __del__(self):
        pygame.display.quit()
    pass