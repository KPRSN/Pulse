"""
Karl Persson, Mac OSX 10.8.4/Windows 8, Python 2.7.5, Pygame 1.9.2pre

Class representing a ball/orb
"""

import pygame, math, time, random
from pygame.locals import *

import Entity

# Representing a ball. Only to be used as a parent.
class Ball(Entity.Entity):
    # Constructor
    def __init__(self, fileManager, gameObjects, scale, hidden, position, direction, baseSpeed, texture, radius):
        super(Ball, self).__init__(fileManager, scale)
        
        self.WINDOW_SIZE = (800, 600)   
        self.radius = radius
        
        # Saving reference to game objects (to add explosions)
        self.gameObjects = gameObjects    
        
        # State: 0 = Alive, 1 = Hit, 2 = Exploding
        self.state = 0
        self.timeOfImpact = 0
        self.turnTimer = 0
        self.nextTurn = 0
        
        # Initializing surface and rect
        self.image = pygame.transform.scale(texture, (int(radius*2), int(radius*2)))
        self.rect = self.image.get_rect()     
        
        # Generate position if none is specified
        if position == None:
            self.rect.left = random.randint(0, 800-self.rect.width)
            self.rect.top = random.randint(0, 600-self.rect.height)
        else:
            # Starting position (x, y)
            self.rect.center = position 
            
        # Y-Position (for showing and hiding)
        self.posY = self.rect.centery
        
        # Show state: 1=showing, -1=hiding, 0=normal
        # Hiding
        if hidden:
            self.__setHidden()
            self.show()
            # Random showing-delay
            self.showDelay = True
            self.timeOfImpact = time.time() + float(random.uniform(0.2, 1.0))
        else:
            self.showState = 0   
            self.showDelay = False

        # Generate direction if none is specified (radians)
        if direction == None:
            self.direction = float(random.uniform(0.0, 2.0*math.pi))
        else:
            self.direction = direction
            
        # Setting base speed and current sped
        self.speed = self.baseSpeed = baseSpeed 
                
        # Setting float positions, for smoother movements
        self.tempx = float(self.rect.centerx)
        self.tempy = float(self.rect.centery)
            
    # Triggering explosion
    def trigger(self):
        # Hit state
        self.state = 1
        # Setting explosion delay
        self.randomExplosionDelay = random.uniform(-0.3, 0.3)
        # Initializing hit alpha for stage 1
        self.hitAlpha = 0            
        # Starting timer/Setting impact time
        self.timeOfImpact = time.time()
        
    # Explosion triggered by push
    def pushTrigger(self, position, speed=None):
        # Setting standard speed if neccessary
        if speed==None:
            speed = self.baseSpeed*10
        self.__push(speed, position)
        self.trigger()
        
    # Explosion triggered by explosion
    def explosionTrigger(self, explosion):
        # Triggering not allowed in hiding state (to avoid cheating)
        if self.showState != -1:
            speed = (self.baseSpeed*(explosion.imageAlpha/15))
            self.__push(speed, explosion.rect.center)
            self.trigger()
        
    # Showing ball (moving it into the screen)
    def show(self):
        self.showState = 1
    
    # Hiding ball (moving it out of screen)
    def hide(self):
        self.hideVariable = .01
        self.showState = -1
    
    # Checking if it's hidden
    def isHidden(self):
        if self.rect.top >= 600 and self.showState == -1:
            return True
        else:
            return False
        
    # Checking if ball is in normal showing state
    def isNormalState(self):
        if self.showState == 0:
            return True
        else:
            return False
        
    # Update showing position
    def __updateShowingCoordinates(self):
        # Showing
        if self.showState == 1:
            # Saving last Y-value
            old = self.tempy     
            self.tempy += (self.posY - self.tempy) * 0.1
            
            # Changing show state when no more movement occurs
            if int(self.tempy) == int(old):
                self.showState = 0
        # Hiding
        elif self.showState == -1 and self.rect.top < 600:
            # Accelerating
            self.hideVariable *= 2
            self.tempy += self.hideVariable
            
            # Stopping movement/setting dead
            if self.tempy - self.rect.width/2 > 600:
                self.isDead = True    
    
    # Making ball hidden on top of the window
    def __setHidden(self):
        self.rect.bottom = 0
        
    # Updating hit object(updating stage 1)
    def __objectHit(self):     
        # Avoiding burning pink color
        if self.hitAlpha < 100:
            # Filling with red (making it pink)
            self.image.fill((5, 0, 0, 0), rect=self.image.get_rect(), special_flags=BLEND_RGBA_ADD)
            # Keeping track of pinkish-level
            self.hitAlpha += 5
    
    # Controlling wall hits
    def __checkWallHits(self, excludeTop=False):
        # Only when ball isn't exploding
        if self.state != 2:
            radius = self.radius        
            hit = False
            
            # X-Check
            # Check right
            if self.tempx + radius > self.WINDOW_SIZE[0]:
                self.direction = (self.direction+math.pi)*-1
                self.tempx = self.WINDOW_SIZE[0] - radius
                hit = True
            # Check left
            elif self.tempx - radius < 0:
                self.tempx = 0 + radius
                self.direction = (self.direction+math.pi)*-1
                hit = True
            # Y-Check
            #Check bottom
            if self.tempy + radius > self.WINDOW_SIZE[1]: 
                self.direction = self.direction * -1
                self.tempy = self.WINDOW_SIZE[1] - radius
                hit = True
            # Check top
            elif self.tempy - radius < 0 and not excludeTop:
                self.direction = self.direction * -1
                self.tempy = 0 + radius
                hit = True
                
            if hit:
                self.fileManager.playWall()
                self.__randomizeDirection()
                # Bounce friction
                if self.speed > self.baseSpeed:
                    self.speed = (self.speed - self.baseSpeed) * 0.6
        
    # Getting pushed
    def __push(self, speed, position):
        self.speed = speed
        # Calculating direction
        vector = ((float(self.rect.center[0] - position[0])), float(self.rect.center[1] - position[1]))
        self.direction = math.atan2(vector[1], vector[0])
        
    # Randomizing direction changes
    def __randomizeDirection(self):
        # Making a new turn (controlled by timer)
        if time.time() > self.turnTimer+self.nextTurn:
            self.turnFactor = random.uniform(-0.05, 0.05)
            self.turnTimer = time.time()
            self.nextTurn = random.uniform(0.8, 2.0)
        # Updating movement
        self.direction += self.turnFactor
        
    # Update direction
    def __updateCoordinates(self):
        # Updating showing coordinates when showing or hiding
        if self.showState != 0:
            self.__updateShowingCoordinates()
            
        # Calculating and saving new coordinates as float     
        self.tempx += self.speed*math.cos(self.direction)
        self.tempy += self.speed*math.sin(self.direction)
            
        # Setting new directions to rect
        self.rect.centerx = int(self.tempx)
        self.rect.centery = int(self.tempy)
        
    # Updating object
    def update(self):
        # Friction if speed is too high (not when exploding)
        if self.speed > self.baseSpeed and self.state != 2:
            self.speed = self.speed - 0.020*self.scale
            if self.speed < 0.0:
                self.speed = 0.0
        
        # Randomizing direction when not being hit (turning)
        if self.state != 1:
            self.__randomizeDirection()  
            
        # Normalizing direction (more than 2*pi/360 degrees is unnecessary)
        while self.direction >= 2 * math.pi:
            self.direction -= 2 * math.pi
        while self.direction <= -2 * math.pi:
            self.direction += 2 * math.pi
        
        # Checking if object is hit
        if self.state > 0:
            self.__objectHit()

        # Checking for wall hits
        if self.showState == 0:
            self.__checkWallHits()
        # Excluding top if balls are showing (droping into screen)
        elif self.showState == 1:
            self.__checkWallHits(True)
            
        # Will wait for show delay to update coordinates
        if self.showDelay:
            if self.timeOfImpact < time.time():
                self.__updateCoordinates()
                self.showDelay = False
        else:
            self.__updateCoordinates()