from wpilib.command.command import Command
from stopwatch import Stopwatch

class DriveTime(Command):
    '''
    classdocs
    '''
    _start_time = None
    _duration = None
    _speed = None
    _stopwatch = None

    def __init__(self, robot, duration, speed, name=None, timeout=None):
        '''
        Constructor
        '''
        super().__init__(name, timeout)
        self.robot = robot;
        self.requires(robot.drivetrain)
        self._duration = duration
        self._speed = speed
        self._stopwatch = Stopwatch()

    def initialize(self):
        """Called before the Command is run for the first time."""
        # Start stopwatch
        self._stopwatch.start()
        return Command.initialize(self)

    def execute(self):
        """Called repeatedly when this Command is scheduled to run"""
        # TODO: implement speed ramp/step so that we don't overshoot target
        self.robot.drivetrain.arcade_drive(self._speed, 0.0)
        return Command.execute(self)

    def isFinished(self):
        """Returns true when the Command no longer needs to be run"""
        # If elapsed time is more than duration
        return self._stopwatch.elapsed_time_in_secs() >= self._duration

    def end(self):
        """Called once after isFinished returns true"""
        self._stopwatch.stop()
        # Stop driving
        self.robot.drivetrain.arcade_drive(0.0, 0.0)

    def interrupted(self):
        """Called when another command which requires one or more of the same subsystems is scheduled to run"""
        self.end()
