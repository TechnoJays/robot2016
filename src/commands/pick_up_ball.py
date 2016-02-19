'''
Created on Feb 18, 2016

@author: tylerstrayer
'''
from wpilib.command.command import Command

class PickUpBall(Command):
    
    _feeder_speed = 0.5
    
    def __init__(self, robot, feeder_speed, name=None, timeout=None):
        '''
        Constructor
        '''
        super().__init__(name, timeout)
        # Read feeder_speed from config
        self.robot = robot
        self._feeder_speed = 0.5
        self.requires(robot.feeder.Class)

    def initialize(self):
        """Called before the Command is run for the first time."""
        return Command.initialize(self)

    def execute(self):
        """Called repeatedly when this Command is scheduled to run"""
        self.robot.feeder.spinFeeder(self._feeder_speed)

    def isFinished(self):
        """Returns true when the Command no longer needs to be run"""
        return self.robot.feeder.hasBall()

    def end(self):
        """Called once after isFinished returns true"""
        pass

    def interrupted(self):
        """Called when another command which requires one or more of the same subsystems is scheduled to run"""
        pass
