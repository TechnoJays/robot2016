'''
Created on Feb 6, 2016

@author: tylerstrayer
'''
from wpilib.command.subsystem import Subsystem

class Feeder(Subsystem):
    
    def __init__(self, robot, name=None):
        pass
    
    def initDefaultCommand(self):
        return Subsystem.initDefaultCommand(self)
    
    def spinFeeder(self, speed):
        """Spins the feeder in the given direction at a speed represented as a float"""
        pass
    
    def hasBall(self):
        return False
    