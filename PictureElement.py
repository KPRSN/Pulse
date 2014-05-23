"""
Karl Persson, Mac OSX 10.8.4/Windows 8, Python 2.7.5, Pygame 1.9.2pre

Image element for use in menues
Inherits from MenuElement
"""

import pygame, MenuElement
from pygame.locals import *

# Class representing an image element in the menu
class PictureElement(MenuElement.MenuElement):
    def __init__(self, picture, pos=(0,0)):
        super(PictureElement, self).__init__(pos)
        
        # Initializing image and rect
        self.image = picture
        self.rect = self.image.get_rect()
        self.rect.center = pos
        
        # X-position as float, for smooth movement
        self.posX = float(self.rect.centerx)