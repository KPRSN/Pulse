"""
Karl Persson, Mac OSX 10.8.4/Windows 8, Python 2.7.5, Pygame 1.9.2pre

Class representing a multiball in game
Spawning four normal balls on impact
"""

import pygame
from pygame.locals import *
import Ball, NormalBall, time, math

# Representing a multiball, releasing normal balls when exploding. Inherits from Ball.
class MultiBall(Ball.Ball):
    # Constructor
    def __init__(self, fileManager, gameObjects, scale, hidden=False, position=None, direction=None):
        # fileManager, gameObjects, scale, hidden, position, direction, baseSpeed, texture, radius
        super(MultiBall, self).__init__(fileManager, gameObjects, scale, hidden, position, direction, scale/10.0, fileManager.multiBallTexture, 10*scale)
        
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
        super(MultiBall, self).update()
        
        # Testing if it's  time to explode/Exploding
        if(self.state == 1 and self.timeOfImpact and time.time() > self.timeOfImpact+1.2 + self.randomExplosionDelay):
            self.state = 2      
            # Temporary variable for calculated position
            position = [0,0]
            # Creating normal balls
            for x in range(0, 4):
                # Calculating direction and position (X, Y)
                direction = math.pi/4 + x*math.pi/2
                position[0] = 2*math.cos(direction)+self.rect.centerx
                position[1] = 2*math.sin(direction) +self.rect.centery
             
                # Creating ball
                tempBall = NormalBall.NormalBall(self.fileManager, self.gameObjects, self.scale, False, position, 0)
                # Pushing ball
                tempBall.pushTrigger(self.rect.center)
                # Adding ball
                self.gameObjects.addEntity(tempBall)
                
            # Playing sound
            self.fileManager.playBallExplode('MultiBall')
                
        # Updating explosion
        if self.state == 2:
            self.__exploding()