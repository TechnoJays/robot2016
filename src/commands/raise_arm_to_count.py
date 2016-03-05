'''
Created on Feb 6, 2016

@author: tylerstrayer
'''
from wpilib.command.command import Command


class RaiseArmToCount(Command):

    def __init__(self, robot, raise_speed, stop_count = 0, name=None, timeout=15):
        '''
        Constructor
        '''
        super().__init__(name, timeout)
        self._robot = robot
        self._raise_speed = raise_speed
        self._stop_count = stop_count
        self.requires(robot.arm)

    def initialize(self):
        """Called before the Command is run for the first time."""
        return Command.initialize(self)

    def execute(self):
        """Called repeatedly when this Command is scheduled to run"""
        self._robot.arm.move_arm(self._raise_speed)

    def isFinished(self):
        """Returns true when the Command no longer needs to be run"""
        return self._robot.arm.get_encoder_value() <= self._stop_count or self.isTimedOut()

    def end(self):
        """Called once after isFinished returns true"""
        self._robot.arm.move_arm(0)

    def interrupted(self):
        """Called when another command which requires one or more of the same subsystems is scheduled to run"""
        self.end()
