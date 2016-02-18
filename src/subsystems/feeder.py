'''
Created on Feb 6, 2016

@author: tylerstrayer
'''
from wpilib.command.subsystem import Subsystem

class Direction(object):
    """Enumerates feeder direction"""
    IN = 0
    OUT = 1

class Feeder(Subsystem):
    
    def __init__(self, robot, name=None):
        pass
    
    def initDefaultCommand(self):
        return Subsystem.initDefaultCommand(self)

    def spinFeeder(self, direction):
        pass
    
    def hasBall(self):
        return False
    