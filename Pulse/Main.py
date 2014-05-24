"""
Karl Persson, Mac OSX 10.8.4/Windows 8, Python 2.7.5, Pygame 1.9.2pre

Main class for Pulse game
"""

import sys
import pygame
from pygame.locals import *

import Explosion, FileManager, GameObjects, HUD, LevelManager, Menues

# The main class of Pulse
class PulseGame:
    def __init__(self):
        pygame.init()
        
        # Initializing file manager and loading icon
        self.fileManager = FileManager.FileManager('Textures', 'Sounds')
        
        # Display properties
        pygame.display.set_icon(self.fileManager.icon)
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption('Pulse')
        
        # Setting background
        self.fileManager.loadBackground()
        self.background = self.fileManager.backgroundTexture
        # Display update
        self.cleanWindow()
        pygame.display.flip()
        
        # Initializing game files
        self.fileManager.loadGameFiles()   
        # Initializing game objects
        self.gameObjects = GameObjects.GameObjects()
        # Initializing level manager
        self.levelManager = LevelManager.LevelManager(self.fileManager, self.gameObjects)
        # Initializing menues
        self.menues = Menues.Menues(self.fileManager, self.levelManager)
        
        # Initializing HUD
        self.HUD = pygame.sprite.RenderPlain()
        self.HUDObject = HUD.HUD(self.levelManager.currentLevel(), True)
        self.HUD.add(self.HUDObject)
        
        # Adding notifieras to gameObjects
        self.gameObjects.addNotifier(self.HUDObject)
        self.gameObjects.addNotifier(self.levelManager)
        
        # Initializing clock
        self.clock = pygame.time.Clock()
        
        # Game running. Showing nenu on False.
        self.gameRunning = False
        
        # Starting music
        pygame.mixer.music.play(-1)
        
        # Showing main menu
        self.menues.main()
        
    # Rendering and updating game (fill old elements with background, update elements, draw new elements)
    def render(self):
        # Adding rects to update on screen
        rects = []
        
        # Erasing previous balls
        # (Blitting to screen and saving rect-copies for updating)
        for sprite in self.gameObjects.allSprites:
            self.screen.blit(self.background, sprite.rect.topleft, sprite.rect)
            rects.append(sprite.rect.copy())
        # Erasing HUD
        self.screen.blit(self.background, self.HUDObject.rect.topleft, self.HUDObject.rect)
        rects.append(self.HUDObject.rect.copy())
        # Erasing menues
        for rect in self.menues.getRects():
            self.screen.blit(self.background, rect.topleft, rect)
            rects.append(rect.copy())
        
        # Updating stuff
        self.update()
        
        # Rendering
        # Sprites
        self.gameObjects.render(self.screen)
        for sprite in self.gameObjects.allSprites:
            rects.append(sprite.rect)
        # HUD
        self.HUD.draw(self.screen)
        rects.append(self.HUDObject.rect)
        # Menu
        self.menues.render(self.screen) 
        for rect in self.menues.getRects():
            rects.append(rect)
            
        # Updating specific rects on screen, for better framerate
        pygame.display.update(rects)
        
    # Updating game
    def update(self):
        # Updating game objects, HUD, menues etc.
        self.gameObjects.update()
        self.HUD.update()
        self.menues.update(pygame.mouse.get_pos())
        
        # Checking game status
        if self.levelManager.playerWon():
            self.gameRunning = False
            # opening menu if it's not already open
            if not self.menues.menuActive():
                # Checking if it's the last level
                if self.levelManager.lastLevel():
                    self.menues.gameWon()
                else:
                    self.menues.levelWon()
        elif self.levelManager.playerLost():
            self.gameRunning = False
            # Opening menu if it's not already open
            if not self.menues.menuActive():
                self.menues.levelLost()
        else:
            # If the game was previously not running hud and background will be reset
            if not self.gameRunning:
                #self.cleanWindow()
                self.HUDObject.setLevel(self.levelManager.currentLevel())
                # Making sure HUD isn't hidden
                self.HUDObject.show()
            self.gameRunning = True
            
    # Cleaning window (blitting background)
    def cleanWindow(self):
        self.screen.blit(self.background, (0,0))
    
if __name__ == '__main__':
    game = PulseGame()
    
    # Game loop
    while True:
        # 60Hz framerate
        game.clock.tick(60)
        game.render()
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN and event.button == 1:
                if game.gameRunning:
                    # Only creating a pulse when the number of pulses left i sufficient
                    if game.levelManager.pulses > 0:
                        # Creating explosion
                        game.gameObjects.addEntity(Explosion.Explosion(game.fileManager, game.levelManager.currentLevel().scale, pygame.mouse.get_pos()))
                        game.gameObjects.updateNotifierPulses(-1)
                        game.fileManager.playPulse()
                else:
                    # Checking menu mouse over (gameRunning False means menu!)
                    game.menues.mouseClicked(pygame.mouse.get_pos())
                