"""
Karl Persson, Mac OSX 10.8.4/Windows 8, Python 2.7.5, Pygame 1.9.2pre

Class representing a game level.
Keeping track of level attributes.
"""

# Class representing a game level
class Level:
    def __init__(self, scale, balls, multiballs, pulses, level):
        self.scale = scale
        self.balls = balls
        self.multiballs = multiballs
        self.pulses = pulses
        self.level = level
        
    # Calculating total number of balls
    def totalPoints(self):
        return (self.balls + (5*self.multiballs))