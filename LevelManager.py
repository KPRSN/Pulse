"""
Karl Persson, Mac OSX 10.8.4/Windows 8, Python 2.7.5, Pygame 1.9.2pre

Class handling levels
"""

import pygame
from pygame.locals import *

import NormalBall, MultiBall

# Class controling game levels
class LevelManager:
    # Initializing level manager with the first level
    def __init__(self, fileManager, gameObjects):
        # Reference to fileManager, for entity creation
        self.fileManager = fileManager
        # Reference to gameObjects, for managing levels
        self.gameObjects = gameObjects
        # Fetching levels
        self.levels = fileManager.loadLevels()
        
        self.currentIndex = 0
        self.pulses = 0
        self.points = 0
    
    # Setting level by index
    def setLevel(self, index):
        # Checking for valid index
        if(index >= 0 and index < len(self.levels)):
            # Current level index
            self.currentIndex = index
            
            # Initializing level variables
            self.points = 0
            self.pulses = self.currentLevel().pulses
            
            # Creating balls (normal and multi)
            for i in range(0, self.currentLevel().balls):
                self.gameObjects.addEntity(NormalBall.NormalBall(self.fileManager, self.gameObjects, self.currentLevel().scale, True))
            for i in range(0, self.currentLevel().multiballs):
                self.gameObjects.addEntity(MultiBall.MultiBall(self.fileManager, self.gameObjects, self.currentLevel().scale, True))
    
    # Restarting level
    def restartLevel(self):
        self.gameObjects.hideBalls()
        self.setLevel(self.currentIndex)
    
    # Setting next level
    def setNext(self):
        self.setLevel(self.currentIndex + 1)
    
    # Setting previous level
    def setPrevious(self):
        self.setLevel(self.currentIndex - 1)
    
    # Get current level
    def currentLevel(self):
        return self.levels[self.currentIndex]
    
    # Checking if player won
    def playerWon(self):
        if(len(self.gameObjects.allBalls) == 0):
            return True
        else:
            return False
    
    # Checking if player lost
    def playerLost(self):
        if((self.pulses <= 0) and 
           (len(self.gameObjects.allExplosions) == 0) and
           (not self.gameObjects.activeBalls())):
            return True
        else:
            return False
        
    # Checking if the last level is reached
    def lastLevel(self):
        if(self.currentIndex < len(self.levels) - 1):
            return False
        else:
            return True
        