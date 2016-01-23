'''
Created on Jan 23, 2016

@author: Ty Strayer
'''
from wpilib.command.command import Command
from subsystems.drivetrain import Drivetrain

class TankDrive(Command):
    '''
    classdocs
    '''
    
    def __init__(self, robot, name=None, timeout=None):
        '''
        Constructor
        '''
        self.requires(Drivetrain)
        super().__init__(name, timeout)
        self.robot = robot;

    def initialize(self):
        """Called before the Command is run for the first time."""
        return Command.initialize(self)

    def execute(self):
        """Called repeatedly when this Command is scheduled to run"""
        return Command.execute(self)

    def isFinished(self):
        """Returns true when the Command no longer needs to be run"""
        return False

    def end(self):
        """Called once after isFinished returns true"""
        pass

    def interrupted(self):
        """Called when another command which requires one or more of the same subsystems is scheduled to run"""
        pass
