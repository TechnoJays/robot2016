'''
Created on Jan 23, 2016

@author: Ty Strayer
'''
from wpilib.command.subsystem import Subsystem
from commands.tank_drive import TankDrive

class Drivetrain(Subsystem):
    '''
    classdocs
    '''
    
    def __init__(self, robot, name = None):
        super().__init__(name = name)
        self.robot = robot;

    def initDefaultCommand(self):
        self.setDefaultCommand(TankDrive(self.robot))
    
    def tankDrive(self, leftSpeed, rightSpeed):
        pass