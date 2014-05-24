"""
Karl Persson, Mac OSX 10.8.4/Windows 8, Python 2.7.5, Pygame 1.9.2pre

Class representing a menu element
Superclass of PictureElement and TextElement
"""

import pygame
from pygame.locals import *

# Representing an element in the menu system (superclass of TextElement and PictureElement)
class MenuElement(pygame.sprite.Sprite):
    # Initialize with position and text content
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)
        
        # X-position saved as float, for smooth movement
        self.posX = float(pos[0])
        
    # Checking if mouse is over object
    def mouseOver(self, pos):
        if(self.rect.collidepoint(pos)):
            return True
        else:
            return False
        
    # Setting float-position to rect
    def refreshPosition(self):
        self.rect.centerx = int(self.posX)
        
    # Updating - Only refreshing position by default
    def update(self, pos=(0,0)):
        self.refreshPosition()
    