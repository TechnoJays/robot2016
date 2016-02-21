'''
Created on Feb 19, 2016

@author: tylerstrayer
'''
from wpilib.command.command import Command
from oi import UserController, JoystickAxis


class MoveArmAnalog(Command):

    def __init__(self, robot, lower_stop_count, raise_stop_count = 0, name=None, timeout=None):
        '''
        Constructor
        '''
        super().__init__(name, timeout)
        self._robot = robot
        self._lower_stop_count = lower_stop_count
        self._raise_stop_count = raise_stop_count
        self.requires(robot.arm)

    def initialize(self):
        """Called before the Command is run for the first time."""
        return Command.initialize(self)

    def execute(self):
        """Called repeatedly when this Command is scheduled to run"""
        move_speed = self._robot.oi.get_axis(UserController.SCORING, JoystickAxis.RIGHTY);
        arm_count = self._robot.arm.get_encoder_value()
        #if self._raise_stop_count <= arm_count <= self._lower_stop_count:
        #    self._robot.arm.move_arm(move_speed)
        #else:
        #    self._robot.arm.move_arm(0)
        self._robot.arm.move_arm(move_speed)

    def isFinished(self):
        """Returns true when the Command no longer needs to be run"""
        return False

    def end(self):
        """Called once after isFinished returns true"""
        self._robot.arm.move_arm(0)

    def interrupted(self):
        """Called when another command which requires one or more of the same subsystems is scheduled to run"""
        self.end()
