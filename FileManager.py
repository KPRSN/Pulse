"""
Karl Persson, Mac OSX 10.8.4/Windows 8, Python 2.7.5, Pygame 1.9.2pre

Class taking care of all file actions ingame
- Levels
- Textures
- Sounds
"""

import pygame
from pygame.locals import *

import sys, Level, os, random

# Class taking care of all file actions
class FileManager:
    # Constructor
    def __init__(self, textureDir, soundDir):
        self.textureDir = textureDir
        self.soundDir = soundDir
        
        self.__initIcon()
        
    # Initializing game files
    def loadGameFiles(self):
        self.__initTextures()
        self.__initSounds()
        
    # Initializing background
    def loadBackground(self):
        self.backgroundTexture = pygame.image.load(self.textureDir+'/background.png').convert()
        
    # Initializing icon
    def __initIcon(self):
        self.icon = pygame.image.load(self.textureDir+'/icon.png')
        
    # Initializing all textures
    def __initTextures(self):
        try:
            # Loading menu textures
            self.logoTexture = pygame.image.load(self.textureDir+'/logo.png').convert_alpha()
            self.instructionsTexture = pygame.image.load(self.textureDir+'/instructions.png').convert_alpha()
            self.ccMusicTexture = pygame.image.load(self.textureDir+'/cc_music.png').convert_alpha()
            
            # Loading entity textures
            self.explosionTexture = pygame.image.load(self.textureDir+'/explosion.png').convert_alpha()
            self.normalBallTexture = pygame.image.load(self.textureDir+'/ball.png').convert_alpha()
            self.multiBallTexture = pygame.image.load(self.textureDir+'/multiball.png').convert_alpha()
            
        except pygame.error:
            sys.exit('Texture error!')
            
    # Initializing all sound
    def __initSounds(self):
        try:
            # Initializing mixer (CD-quality)
            pygame.mixer.init(frequency=44100, size=16, channels=2, buffer=4096)
            # Larger number of playback channels (default = 8)
            pygame.mixer.set_num_channels(48)
            # Reserving channels 
            pygame.mixer.set_reserved(36)
            
            # Lists of reserved channels
            self.normalBallChannels = []
            self.multiBallChannels = []
            self.wallChannels = []
            self.pulseChannels = []
            
            # Setting reserved channels
            # Normal ball 16 channels
            for i in range(0, 15):
                self.normalBallChannels.append(pygame.mixer.Channel(i))
            # Multiball 8 channels
            for i in range(16, 23):
                self.multiBallChannels.append(pygame.mixer.Channel(i))
            # Wall 6 channels
            for i in range(24, 29):
                self.wallChannels.append(pygame.mixer.Channel(i))
            # Pulse 6 channels
            for i in range(30, 35):
                self.pulseChannels.append(pygame.mixer.Channel(i))
            
            # Loading Music
            pygame.mixer.music.load(self.soundDir+'/Frame-North_sea.ogg')
            pygame.mixer.music.set_volume(0.15)
            
            # Loading sounds
            self.normalBallSounds = self.__loadSounds('NormalBall')
            self.multiBallSounds = self.__loadSounds('MultiBall')
            self.wallSounds = self.__loadSounds('Wall')
            self.pulseSound = pygame.mixer.Sound(self.soundDir+'/pulse.ogg')
            
        except pygame.error:
            exit('Sound error!')
            
    # Loading levels from file
    def loadLevels(self):
        # Container for all levels
        levels = []
        levelNr = 0
        # Trying to read levels-file
        try:
            file = open('levels', mode = 'r')
            # Reading lines in file/levels
            for line in file:
                # Not adding comments
                if(line[:1] != '#'):
                    # Splitting line by whitespaces
                    settings = line.split()
                    # Only creating level by valid settings
                    if(len(settings) == 4):
                        try:
                            scale = float(settings[0])
                            balls = int(settings[1])
                            multiballs = int(settings[2])
                            pulses = int(settings[3])
                            levelNr += 1
                            
                            # Adding to list
                            levels.append(Level.Level(scale, balls, multiballs, pulses, levelNr)) 
                        except ValueError:
                            pass
            # Return all levels; error if no levels 
            if(len(levels) > 0):
                return levels
            else:
                exit('Level error!')     
        except IOError:
            exit('Level error!')
            
            
    # Playback methods
    # Playing ball exploding sound
    def playBallExplode(self, ballType):
        sound = None
        
        # Randomizing sound
        if ballType == 'NormalBall':
            if len(self.normalBallSounds) > 0:
                # Fetching sound
                sound = self.normalBallSounds[random.randint(0, len(self.normalBallSounds)-1)]
                # Fetching channel
                channel = self.getFreeChannel(self.normalBallChannels)
        elif ballType == 'MultiBall':
            if len(self.multiBallSounds) > 0:
                sound = self.multiBallSounds[random.randint(0, len(self.multiBallSounds)-1)]        
                channel = self.getFreeChannel(self.multiBallChannels)
        # Only playing if there are any specified sound
        if sound and channel:
            # Randomizing volume and playing sound
            channel.set_volume(random.uniform(0.5, 1.0))
            channel.play(sound)
    
    # playing pulse sound
    def playPulse(self):
        channel = self.getFreeChannel(self.pulseChannels)
        if channel:
            channel.play(self.pulseSound)
    
    # Playing wall bounce sound
    def playWall(self):
        # Only playing if there are any sounds to play
        if len(self.wallSounds) > 0:
            # Fetching free channel, and playing on that channel
            channel = self.getFreeChannel(self.wallChannels)
            if channel:
                # Randomizing sound
                soundIndex = random.randint(0, len(self.wallSounds)-1)          
                # Randomizing volume
                channel.set_volume(random.uniform(0.3, 0.5))
                # Playing sound
                channel.play(self.wallSounds[soundIndex])
            
    # Get free audio channel from list of reserved ones
    def getFreeChannel(self, channels):
        # Searching for free channel
        for channel in channels:
            if not channel.get_busy():
                return channel
        return None
    
    # Loading multiball sounds
    def __loadSounds(self, folder):
        directory = self.soundDir + '/' + folder
        sounds = []
        try:
            # Loading all sounds files
            for soundFile in os.listdir(directory):
                # Making sure only ogg files are used
                if soundFile[-3:] == 'ogg':
                    sounds.append(pygame.mixer.Sound(directory + '/' + soundFile))
        except pygame.error:
            exit('Sound error!')
        return sounds
    
    
    
        