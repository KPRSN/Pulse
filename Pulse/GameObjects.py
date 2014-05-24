"""
Karl Persson, Mac OSX 10.8.4/Windows 8, Python 2.7.5, Pygame 1.9.2pre

Class controlling all of the game objects.
"""

import pygame, math
from pygame.locals import *

# Class controlling all game objects
class GameObjects():
    def __init__(self):
        # Reset variable for delayed reset (balls hiding)
        self.waitingReset = False
        # initializing sprite groups
        self.reset()
        # Initializing list for objects to be notified by changes
        self.notifiers = []
        
    # Drawing entities on the right screen
    def render(self, screen):
        self.allBalls.draw(screen)
        self.allExplosions.draw(screen)
        
        
    # Updating entities
    def update(self):
        self.removeDead()
        self.allSprites.update()
        self.checkExplosionHits()
        
        # Checking if it's time to execute waiting reset (waiting for normal-state-balls)
        if self.waitingReset and self.isNormalState():
            self.reset(force=True)
            self.waitingReset = False
        
    # Removing dead objects
    def removeDead(self):
        for entity in self.allSprites:
            if entity.isDead:
                # Removing sprite from all groups
                entity.kill()      
                # Updating points is superclass is Ball
                # Will only give points for sprites on screen (avoid cheating)
                if (self.__isSubclass(entity, 'Ball') and not entity.isHidden()):
                    self.updateNotifierPoints(1)
                
    # Checking for explosion hits
    def checkExplosionHits(self):
        for ball in self.allBalls:
            for explosion in self.allExplosions:
                if(pygame.sprite.collide_mask(ball, explosion) and
                   ball.state == 0):
                    ball.explosionTrigger(explosion)
                                        
    # Adding entity/sprite to the game objecs
    def addEntity(self, entity):
        # Checking object type
        # Checking if superclass is ball or if class is explosion
        #if ('Ball' in superclasses):
        if (self.__isSubclass(entity, 'Ball')):
            self.allBalls.add(entity)
            self.allSprites.add(entity)
            return True
        elif (type(entity).__name__ == 'Explosion'):
            self.allExplosions.add(entity)
            self.allSprites.add(entity)
            return True
        else:
            return False
        
    # Checking for active balls
    def activeBalls(self):
        counter = 0
        # Counting active balls
        for ball in self.allBalls:
            if ball.state > 0:
                counter += 1
        
        # Returning True if there are any active balls
        if counter > 0:
            return True
        else:
            return False
        
    # Checking if entity has a specific parent
    def __isSubclass(self, entity, superclassName):
        # For saving superclass names
        superclasses = []
        # Fetching names of superclasses
        for superclass in type(entity).__bases__:
            superclasses.append(superclass.__name__)
        # Testing if superclass
        if (superclassName in superclasses):
            return True
        else:
            return False
            
    
    
    # Adding objects that should be updated by game progress (points taken+pulses left)
    def addNotifier(self, notifier):
        # Making sure attributes exist, and adding to list
        if (hasattr(notifier, 'pulses') and hasattr(notifier, 'points')):
            self.notifiers.append(notifier)
            
    # Updating notifier pulses by number difference
    def updateNotifierPulses(self, pulses):
        for n in self.notifiers:
            n.pulses += pulses
    
    # Updating notifier points by number difference
    def updateNotifierPoints(self, points):
        for n in self.notifiers:
            n.points += points
            
    # Hide balls
    def hideBalls(self):
        for ball in self.allBalls:
            ball.hide()
            
    # Returning True if all balls is in normal showing state (not hiding/showing)
    def isNormalState(self):
        for ball in self.allBalls:
            if not ball.isNormalState():
                return False
        return True
            
    # Clearing all objects
    def reset(self):
        self.allBalls = pygame.sprite.RenderPlain()
        self.allExplosions = pygame.sprite.RenderPlain()
        self.allSprites = pygame.sprite.RenderPlain()