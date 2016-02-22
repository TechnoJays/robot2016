'''
Created on Feb 6, 2016

@author: tylerstrayer
'''
from wpilib.command.command import Command

from oi import JoystickAxis, UserController


class FeedBallAnalog(Command):
    
    def __init__(self, robot, max_speed, name=None, timeout=None):
        '''
        Constructor
        '''
        super().__init__(name, timeout)
        self._max_pickup_speed = max_speed
        self.robot = robot
        self.requires(robot.feeder)

    def initialize(self):
        """Called before the Command is run for the first time."""
        return Command.initialize(self)

    def execute(self):
        """Called repeatedly when this Command is scheduled to run"""
        speed = self.robot.oi.get_axis(UserController.SCORING, JoystickAxis.LEFTY)
        self.robot.feeder.spinFeeder(self._max_speedspeed)

    def isFinished(self):
        """Returns true when the Command no longer needs to be run"""
        return False

    def end(self):
        """Called once after isFinished returns true"""
        self.robot.feeder.spinFeeder(0)

    def interrupted(self):
        """Called when another command which requires one or more of the same subsystems is scheduled to run"""
        self.end()
