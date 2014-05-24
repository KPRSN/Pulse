"""
Karl Persson, Mac OSX 10.8.4/Windows 8, Python 2.7.5, Pygame 1.9.2pre

Class handling the HUD, showing number of pulses, current level etc.
"""

import pygame
from pygame.locals import *

# Class controlling the head up display
class HUD(pygame.sprite.Sprite):
    def __init__(self, level, hidden=False):
        # Init pygame sprite
        pygame.sprite.Sprite.__init__(self)
        
        self.WINDOW_SIZE = (600, 800)
        self.__hidden = False
        
        # Initializing font
        self.font = pygame.font.Font('neuropol.ttf', 20)
        self.fontColor = pygame.Color(255, 255, 255)
        
        # Saving Y-axis position
        self.bottomPos = self.WINDOW_SIZE[0]-5
        
        # Initializing surface containing HUD-elements
        self.image = pygame.surface.Surface((800, 20)).convert()
        self.image.set_colorkey((0,0,0))
        self.rect = self.image.get_rect()
        
        # Setting position
        if hidden:
            self.__setHidden()
        else:
            self.posY = float(self.bottomPos)
            
        self.__updatePosition()
        self.setLevel(level)
        
    # Setting level to HUD
    def setLevel(self, level):
        self.level = level.level
        self.pointsTotal = level.totalPoints()
        self.pulses = level.pulses
        self.points = 0
        
    # Updating and drawing full HUD
    def update(self):
        self.__updateLabels()
        self.__updatePosition()
        
        self.image.fill((0,0,0))
        self.image.blit(self.font.render(self.levelLabel, 1, self.fontColor), (5,0))
        self.image.blit(self.font.render(self.ballsLabel, 1, self.fontColor), (400-self.font.size(self.ballsLabel)[0]/2, 0))   
        self.image.blit(self.font.render(self.pulsesLabel, 1, self.fontColor), (795-self.font.size(self.pulsesLabel)[0], 0))
        
    # Showing HUD
    def show(self):
        self.__hidden = 1
        
    # Updating position (hiding/showing)
    def __updatePosition(self):
        # Checking state and position, and updating position
        if self.__hidden and self.rect.bottom > self.bottomPos:
            self.posY += (self.bottomPos - self.posY) * 0.1
        else:
            self.__hidden = False
            
        # Setting float position to rect
        self.rect.bottom = int(self.posY)
    
    # Updating labels
    def __updateLabels(self):
        self.ballsLabel = (str(self.points) + ' of ' + str(self.pointsTotal))
        self.levelLabel = ('Level ' + str(self.level))
        self.pulsesLabel = (str(self.pulses) + ' pulses left')
        
    # Setting HUD hidden
    def __setHidden(self):
        self.posY = int(self.WINDOW_SIZE[0] + self.rect.height)