'''
Created on Feb 6, 2016

@author: tylerstrayer
'''
from wpilib.command.subsystem import Subsystem
from commands.move_arm_analog import MoveArmAnalog

class ScalingArm(Subsystem):
    
    def __init__(self, robot, name=None):
        pass
    
    def initDefaultCommand(self):
        self.setDefaultCommand(MoveArmAnalog(self._robot, 50))
    