"""
Karl Persson, Mac OSX 10.8.4/Windows 8, Python 2.7.5, Pygame 1.9.2pre

Class representing a normal ball in game
Exploding on impact
"""

import pygame
from pygame.locals import *
import Ball, Explosion, time

# Representing a normal, exploding ball. Inherits from Ball.
class NormalBall(Ball.Ball):
    # Constructor
    def __init__(self, fileManager, gameObjects, scale, hidden=False, position=None, direction=None):
        # fileManager, gameObjects, scale, position, direction, baseSpeed, texture, radius
        super(NormalBall, self).__init__(fileManager, gameObjects, scale, hidden, position, direction, scale/6.0, fileManager.normalBallTexture, 5*scale)
        #Ball.Ball(fileManager, gameObjects, scale, position, direction, scale/6, fileManager.normalBallTexture, 5*scale)
        
    # Exploding
    def __exploding(self):
        # Only exploding when there is something to explode. Otherwise dead.
        if self.rect.width > 0:
            # Calculating shrinkage
            diameter = int(self.rect.width*0.9)
            position = self.rect.center    
            # Avoiding negative numbers
            if(diameter < 0):
                diameter = 0
            
            # Shrinking
            self.image = pygame.transform.smoothscale(self.image, (diameter, diameter))  
            self.rect = self.image.get_rect()
            self.rect.center = position
            # Accelerating
            self.speed += self.scale/2
        else:
            self.isDead = True
          
    # Updating object
    def update(self):
        super(NormalBall, self).update()
        
        # Testing if it's time to explode/Exploding
        if(self.state == 1 and self.timeOfImpact and time.time() > self.timeOfImpact+0.8 + self.randomExplosionDelay):
            self.state = 2
            # Creating explosion
            self.gameObjects.addEntity(Explosion.Explosion(self.fileManager, self.scale, self.rect.center))
            # Playing sound
            self.fileManager.playBallExplode('NormalBall')
        
        # Updating explosion
        if self.state == 2:
            self.__exploding()
        