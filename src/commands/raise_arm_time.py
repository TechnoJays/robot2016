'''
Created on Feb 22, 2016

@author: tylerstrayer
'''
from wpilib.command.command import Command
from stopwatch import Stopwatch

class RaisArmTime(Command):

    def __init__(self, robot, raise_speed, stop_time, name=None, timeout=None):
        '''
        Constructor
        '''
        super().__init__(name, timeout)
        self._robot = robot
        self._raise_speed = raise_speed
        self._stop_time = stop_time
        self.requires(robot.arm)
        self._stopwatch = Stopwatch()

    def initialize(self):
        """Called before the Command is run for the first time."""
        self._stopwatch.start()

    def execute(self):
        """Called repeatedly when this Command is scheduled to run"""
        self._robot.arm.move_arm(self._raise_speed)

    def isFinished(self):
        """Returns true when the Command no longer needs to be run"""
        return self._stopwatch.elapsed_time_in_secs() >= self._stop_time

    def end(self):
        """Called once after isFinished returns true"""
        self._robot.arm.move_arm(0)

    def interrupted(self):
        """Called when another command which requires one or more of the same subsystems is scheduled to run"""
        self.end()
