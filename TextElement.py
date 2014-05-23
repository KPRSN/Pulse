"""
Karl Persson, Mac OSX 10.8.4/Windows 8, Python 2.7.5, Pygame 1.9.2pre

Text element for use in menues
Inherits from MenuElement
"""

import pygame, MenuElement
from pygame.locals import *

# Class representing a text element in the menu
class TextElement(MenuElement.MenuElement):
    def __init__(self, pos, text, font, fontColor=pygame.Color(255,255,255)):
        super(TextElement, self).__init__(pos)

        # Text attributes
        self.text = text
        self.font = font
        self.fontColor = self.currentColor = fontColor
        
        # Creating font image
        self.image = font.render(text, 1, fontColor)
        self.rect = self.image.get_rect()
        self.rect.center = pos
    
    # Handling mouse-over-actions, returning True if mouse-over.
    def update(self, pos):
        # Updating position
        self.refreshPosition()
        
        # Updating color
        if self.mouseOver(pos):
            self.__colorChange(5)
        else:
            self.__colorChange(-5)
                     
        # Updating font
        self.image = self.font.render(self.text, 1, self.currentColor)
            
    # Changing button-color
    def __colorChange(self, factor):
        # Making sure the RGB-code is valid
        if (self.currentColor.r-factor >= 150 and
            self.currentColor.r-factor <= 255):
            self.currentColor.r -= factor
            self.currentColor.g -= factor
    