"""
Karl Persson, Mac OSX 10.8.4/Windows 8, Python 2.7.5, Pygame 1.9.2pre

Entity class
Superclass of all balls and explosions
"""

import pygame
from pygame.locals import *

class Entity(pygame.sprite.Sprite):
    def __init__(self, fileManager, scale):
        # Initialize pygame
        pygame.sprite.Sprite.__init__(self)
        
        self.fileManager = fileManager
        self.scale = scale
        self.isDead = False