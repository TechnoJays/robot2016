'''
Created on Feb 6, 2016

@author: tylerstrayer
'''
from wpilib.command.command import Command

class RetractArmToCount(Command):
    
    def __init__(self, robot, extend_speed, raise_stop_count = 0, name=None, timeout=None):
        '''
        Constructor
        '''
        super().__init__(name, timeout)
        self._robot = robot
        self._extend_speed = extend_speed
        self._raise_stop_count = raise_stop_count
        self.requires(robot.arm)

    def initialize(self):
        """Called before the Command is run for the first time."""
        return Command.initialize(self)

    def execute(self):
        """Called repeatedly when this Command is scheduled to run"""
        self._robot.arm.moveWinch(self._extend_speed)

    def isFinished(self):
        """Returns true when the Command no longer needs to be run"""
        return self._robot.arm.getWinchCount() <= self._raise_stop_count

    def end(self):
        """Called once after isFinished returns true"""
        self._robot_arm.moveWinch(0)

    def interrupted(self):
        """Called when another command which requires one or more of the same subsystems is scheduled to run"""
        self.end()
