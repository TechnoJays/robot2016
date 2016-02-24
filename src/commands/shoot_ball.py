'''
Created on Feb 22, 2016

@author: tylerstrayer
'''
from wpilib.command.commandgroup import CommandGroup
from commands.raise_arm_time import RaisArmTime
from commands.feed_ball_out import FeedBallOut
from configparser import ConfigParser

class ShootBall(CommandGroup):

    SECTION_NAME = "ShootCommand"

    _arm_lift_time = 0.5
    _arm_lift_speed = 1.0
    _feed_out_time = 1.0
    _feed_out_speed = 1.0

    def __init__(self, robot, config_path = "/home/lvuser/configs/commands.ini",name=None):
        CommandGroup.__init__(self, name=name)
        self._config_path = config_path
        self._read_config()
        self.addSequential(RaisArmTime(robot, self._arm_lift_speed, self._arm_lift_time))
        self.addSequential(FeedBallOut(robot, self._feed_out_speed, self._feed_out_time))

    def _read_config(self):
        config = ConfigParser()
        config.read(self._config_path)
        self._arm_lift_time = config.getfloat(ShootBall.SECTION_NAME, "ARM_LIFT_TIME")
        self._arm_lift_speed = config.getfloat(ShootBall.SECTION_NAME, "ARM_LIFT_SPEED")
        self._feed_out_time = config.getfloat(ShootBall.SECTION_NAME, "FEED_OUT_TIME")
        self._feed_out_speed = config.getfloat(ShootBall.SECTION_NAME, "FEED_OUT_SPEED")
