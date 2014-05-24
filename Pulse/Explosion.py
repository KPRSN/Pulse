"""
Karl Persson, Mac OSX 10.8.4/Windows 8, Python 2.7.5, Pygame 1.9.2pre

Class representing an explosion. 
Inherits from Entity.
"""

import pygame
from pygame.locals import *

import Entity

# Class representing an explosion
class Explosion(Entity.Entity):
    # Constructor
    def __init__(self, fileManager, scale, position):
        super(Explosion, self).__init__(fileManager, scale)
        
        # Setting opacity and radius
        self.imageAlpha = 255
        radius = 5*scale
        
        # Setting image     
        self.image = pygame.transform.scale(self.fileManager.explosionTexture, (int(radius*2.2), int(radius*2.2)))
        self.rect = self.image.get_rect()
        self.rect.center = position

    # Updating explosion
    def update(self):  
        # Growing and getting more transparent
        if self.imageAlpha > 0:          
            # Increasing size
            diameter = int(self.rect.width+(self.scale*2.5))
            position = self.rect.center
            # Decreasing opaqueness
            self.imageAlpha -= 10
            # Making sure alpha is not less than zero
            if self.imageAlpha < 0:
                self.imageAlpha = 0
            
            # Making changes
            self.image = pygame.transform.scale(self.fileManager.explosionTexture, (diameter, diameter))        
            self.image.fill((255, 255, 255, self.imageAlpha), None, pygame.BLEND_RGBA_MULT)
            self.rect = self.image.get_rect()
            self.rect.center = position
            
            # Setting collissionmask with an alpha threshold of 50 (0-255)
            self.mask = pygame.mask.from_surface(self.image, 50)
        else:
            # Making dead when the explosion is fully transparent
            self.isDead = True