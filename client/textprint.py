'''
Created on 8/06/2016

@author: phil
'''
import pygame


BLACK    = (   0,   0,   0)
WHITE    = ( 255, 255, 255)    

class TextPrint:
    '''
    This is a simple class that will help us print to the screen
    It has nothing to do with the joysticks, just outputing the information.
    '''
    
    def __init__(self):
        self.reset()
        self.font = pygame.font.Font(None, 20)

    def print(self, screen, textString):
        textBitmap = self.font.render(textString, True, BLACK)
        screen.blit(textBitmap, [self.x, self.y])
        self.y += self.line_height
        
    def reset(self):
        self.x = 10
        self.y = 10
        self.line_height = 15
        
    def indent(self):
        self.x += 10
        
    def unindent(self):
        self.x -= 10
