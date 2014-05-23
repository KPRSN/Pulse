"""
Karl Persson, Mac OSX 10.8.4/Windows 8, Python 2.7.5, Pygame 1.9.2pre

Class handling menues and menu interactions
"""

import pygame
from pygame.locals import *

import PictureElement, TextElement

# Class handling all menu elements
class Menues():
    def __init__(self, fileManager, levelManager, startLevel=0):
        # Saving references to file- and levelmanager etc.
        self.fileManager = fileManager
        self.levelManager = levelManager
        self.startLevel = startLevel
        self.WINDOW_SIZE = (800, 600)
        
        # Setting standard font for menu alternatives
        self.font = pygame.font.Font('neuropol.ttf', 40)
        
        # Set all active buttons to None
        self.__resetActiveElements()
        
        # 1 = Opening, -1 = Closing
        self.state = 0
        
        # Initializing generic menu position (X)
        self.menuCenter = self.WINDOW_SIZE[0]/2
        
    
    # Showing main menu
    def main(self):
        # Creating start-button
        self.buttons['start'] = TextElement.TextElement((self.WINDOW_SIZE[0]/2,280), 'Start', self.font)
        # Adding start button to active buttons (sprite group), for rendering etc.
        self.activeElements.add(self.buttons['start'])
        # Adding logo
        self.activeElements.add(PictureElement.PictureElement(self.fileManager.logoTexture, (self.WINDOW_SIZE[0]/2, 150)))
        # Adding instructions
        self.activeElements.add(PictureElement.PictureElement(self.fileManager.instructionsTexture, (self.WINDOW_SIZE[0]/2, 420)))
        # Adding music info (creative commons)
        self.activeElements.add(PictureElement.PictureElement(self.fileManager.ccMusicTexture, (self.WINDOW_SIZE[0]/2, self.WINDOW_SIZE[1]-self.fileManager.ccMusicTexture.get_height())))
        # Opening menu
        self.state = 1
        self.__setHidden()
    
    # Showing level won menu
    def levelWon(self):
        # Creating next-button
        self.buttons['next'] = TextElement.TextElement((self.WINDOW_SIZE[0]/2, 280), 'Next level', self.font)
        self.activeElements.add(self.buttons['next'])
        # Resetting start level
        self.startLevel = 0
        # Opening menu
        self.state = 1
        self.__setHidden()
    
    # Showing level lost menu
    def levelLost(self):
        # Creating restart-button
        self.buttons['restart'] = TextElement.TextElement((self.WINDOW_SIZE[0]/2, 280), 'Restart level', self.font)
        self.activeElements.add(self.buttons['restart'])
        # Opening menu
        self.state = 1
        self.__setHidden()
    
    # Showing game won menu
    def gameWon(self):
        # Creating next-button
        self.buttons['start'] = TextElement.TextElement((self.WINDOW_SIZE[0]/2, 280), 'Play again', self.font)
        self.activeElements.add(self.buttons['start'])
        # Opening menu
        self.state = 1
        self.__setHidden()
    
    # Closing menu
    def close(self):
        self.state = -1
        
    # Updating and handling mouse-over (hovering)
    def update(self, pos=(-1, -1)):
        self.__updatePosition()
        
        # Updating all active elements
        for element in self.activeElements:
            element.update(pos)
    
    # Handling mouse-clicks (choosing menu alternatives)
    def mouseClicked(self, pos):
        # Checking all buttons for mouse clicks
        if(self.buttons['start'] != None and self.buttons['start'].mouseOver(pos)):
            # Setting starting level
            self.levelManager.setLevel(self.startLevel)
            # Removing menu
            self.state = -1
            # Variable to aid the hide animation
            self.hideVariable = 2
        elif(self.buttons['restart'] != None and self.buttons['restart'].mouseOver(pos)):
            # Restart
            self.levelManager.restartLevel()
            # Removig menu
            self.state = -1
            # Variable to aid the hide animation
            self.hideVariable = 2
        elif(self.buttons['next'] != None and self.buttons['next'].mouseOver(pos)):
            # Next
            self.levelManager.setNext()
            # Removing menu
            self.state = -1
            # Variable to aid the hide animation
            self.hideVariable = 1.0
        
    # Checking if any menu is active
    def menuActive(self):
        if len(self.activeElements) > 0:
            return True
        else:
            return False
        
    # Updating position depending on state
    def __updatePosition(self):
        # Move in
        if self.state == 1:
            # Checking if it's in position
            if self.__getTotalCenter() < self.menuCenter:
                for element in self.activeElements:
                    element.posX += (self.menuCenter - element.posX) * 0.1
            else:
                self.state = 0
        # Move out
        elif self.state == -1:
            # Moving out if it's not already outside window. Otherwise resetting buttons.
            if ((self.__getTotalCenter() - self.__getTotalWidth()/2) < self.WINDOW_SIZE[0]):           
                for element in self.activeElements:
                    # Calculating hiding-animation
                    self.hideVariable *= 1.2
                    element.posX += self.hideVariable
            else:
                self.__resetActiveElements()
    
    # Get total center of the menu (X)
    def __getTotalCenter(self):
        tot = 0.0
        if(len(self.activeElements) > 0):
            for element in self.activeElements:
                tot += element.rect.centerx           
            return int(tot/len(self.activeElements))
        else:
            return 0
    
    # Get total width of the menu
    def __getTotalWidth(self):
        absoluteLeft = 0
        absoluteRight = 0
        firstTest = True
        
        # Fetching extreme values
        for element in self.activeElements:
            # Controlling left
            if element.rect.left < absoluteLeft:
                absoluteLeft = element.rect.left
            # Controlling right
            if element.rect.right > absoluteRight:
                absoluteRight = element.rect.right
            if firstTest:
                absoluteLeft = element.rect.left
                absoluteRight = element.rect.right
                firstTest = False
            
        return absoluteRight-absoluteLeft
    
    # Hide menu on the left side of the screen
    def __setHidden(self):
        # Calculating movement
        moveAmount = 0 - (self.__getTotalCenter()+self.__getTotalWidth())
        # Making movement
        for element in self.activeElements:
            element.posX += moveAmount
            element.refreshPosition()
        
    # Rendering elements to screen
    def render(self, screen):
        self.activeElements.draw(screen)
    
    # Resetting all active buttons to None
    def __resetActiveElements(self):
        self.buttons = {'start': None, 'restart': None, 'next': None}
        self.activeElements = pygame.sprite.RenderPlain()
        
    # Get all active rects
    def getRects(self):
        rects = []   
        for element in self.activeElements:
            rects.append(element.rect)
        return rects