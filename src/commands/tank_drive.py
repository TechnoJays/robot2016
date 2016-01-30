'''
Created on Jan 23, 2016

@author: Ty Strayer
'''

from wpilib.command.command import Command

from oi import JoystickAxis, UserController


class TankDrive(Command):
    '''
    classdocs
    '''
    
    _oi = None
    _tank_drive_enabled = False
    _config = None
    
    def __init__(self, robot, oi, name=None, timeout=None):
        '''
        Constructor
        '''
        self._oi = oi
        super().__init__(name, timeout)
        self.robot = robot;
        self.requires(robot.drivetrain)

    def initialize(self):
        """Called before the Command is run for the first time."""
        return Command.initialize(self)

    def execute(self):
        """Called repeatedly when this Command is scheduled to run"""
        left_track = self._oi.get_axis(UserController.DRIVER, JoystickAxis.LEFTY)
        right_track = self._oi.get_axis(UserController.DRIVER, JoystickAxis.RIGHTY)
        self.robot.drivetrain.tankDrive(left_track, right_track)
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
 