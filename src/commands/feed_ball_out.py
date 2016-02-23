'''
Created on Feb 6, 2016

@author: tylerstrayer
'''
import time

from wpilib.command.command import Command


class FeedBallOut(Command):

    _time_stamp = 0

    def __init__(self, robot, feederSpeed, feed_out_time, name=None, timeout=None):
        '''
        Constructor
        '''
        super().__init__(name, timeout)
        # Read feeder_speed from config
        self._feed_out_time_seconds = feed_out_time
        self._feeder_speed = feederSpeed
        self.robot = robot
        self.requires(robot.feeder.Class)

    def initialize(self):
        """Called before the Command is run for the first time."""
        self._time_stamp = time.time()

    def execute(self):
        """Called repeatedly when this Command is scheduled to run"""
        self.robot.feeder.spinFeeder(self._feeder_speed)

    def isFinished(self):
        """Returns true when the Command no longer needs to be run"""
        return  time.time() > self._time_stamp + self._feed_out_time_seconds

    def end(self):
        """Called once after isFinished returns true"""
        self.robot.feeder.spinFeeder(0)

    def interrupted(self):
        """Called when another command which requires one or more of the same subsystems is scheduled to run"""
        self.end()
