'''
Created on Feb 6, 2016

@author: tylerstrayer
'''
import time

from wpilib.command.command import Command


class FeedBallOut(Command):
    
    _first_execute = True
    _feed_out_time_seconds = 2.0
    _time_stamp = 0
    _feeder_speed = 0.5
    
    def __init__(self, robot, feed_out_time, feederSpeed, name=None, timeout=None):
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
        return Command.initialize(self)

    def execute(self):
        """Called repeatedly when this Command is scheduled to run"""
        if self._first_execute:
            self._time_stamp = time.time()
            self._first_execute = False
        self.robot.feeder.spinFeeder(self._feeder_speed)

    def isFinished(self):
        """Returns true when the Command no longer needs to be run"""
        return  time.time() > self._time_stamp + self._feed_out_time_seconds

    def end(self):
        """Called once after isFinished returns true"""
        self._first_execute = True

    def interrupted(self):
        """Called when another command which requires one or more of the same subsystems is scheduled to run"""
        self._first_execute = True
    