'''
Created on Feb 6, 2016

@author: tylerstrayer
'''
import configparser
import os

from wpilib.command.subsystem import Subsystem
from wpilib.encoder import Encoder
from wpilib.robotdrive import RobotDrive
from wpilib.smartdashboard import SmartDashboard
from wpilib.talon import Talon
from wpilib.victor import Victor

from commands.move_arm_analog import MoveArmAnalog


class Arm(Subsystem):

    _robot = None
    _subsystem_config = None
    _encoder = None
    _speed_ratio = 1.0
    _encoder_value = 0
    _left_motor = None
    _right_motor = None

    def __init__(self, robot, speed_ratio=0.5, name=None, subsystem_config = '/home/lvuser/configs/subsystems.ini', command_config = '/home/lvuser/configs/commands.ini'):
        self._robot = robot;
        self._subsystem_config = subsystem_config
        self._command_config = command_config
        self._speed_ratio = speed_ratio
        self._init_components()
        self._update_smartdashboard(0.0)
        super().__init__(name = name)

    def initDefaultCommand(self):
        config = configparser.ConfigParser()
        config.read(os.path.join(os.getcwd(), self._command_config))
        COMMAND_SECTION = "ArmCommands"

        back_drive_limit = config.getfloat(COMMAND_SECTION, "BACK_DRIVE_LIMIT")
        back_drive_speed = config.getfloat(COMMAND_SECTION, "BACK_DRIVE_SPEED")
        scaling_factor = config.getfloat(COMMAND_SECTION, "SCALING_FACTOR")
        raised_bound = config.getint(COMMAND_SECTION, "RAISED_BOUND")
        self.setDefaultCommand(MoveArmAnalog(self._robot, scaling_factor, back_drive_speed,
                                             back_drive_limit, raised_bound))

    def move_arm(self, speed):
        if self._left_motor:
            self._left_motor.setSpeed(-1.0 * speed * self._speed_ratio)
        if self._right_motor:
            self._right_motor.setSpeed(speed * self._speed_ratio)
        self.get_encoder_value()
        self._update_smartdashboard(speed)

    def get_encoder_value(self):
        if (self._encoder):
            self._encoder_value = self._encoder.get()
        return self._encoder_value

    def reset_encoder_value(self):
        if (self._encoder):
            self._encoder.reset()
            self._encoder_value = self._encoder.get()
        self._update_smartdashboard(0.0)
        return self._encoder_value

    def _update_smartdashboard(self, speed):
        SmartDashboard.putNumber("Arm Encoder", self._encoder_value)
        SmartDashboard.putNumber("Arm Speed", speed)

    def _init_components(self):

        config = configparser.ConfigParser()
        config.read(os.path.join(os.getcwd(), self._subsystem_config))

        RIGHT_MOTOR_SECTION = "ArmRightMotor"
        LEFT_MOTOR_SECTION = "ArmLeftMotor"
        ENCODER_SECTION = "ArmEncoder"
        ENABLED = "ENABLED"
        CHANNEL = "CHANNEL"
        INVERTED = "INVERTED"

        if (config.getboolean(LEFT_MOTOR_SECTION, ENABLED)):
            left_motor_channel = config.getint(LEFT_MOTOR_SECTION, CHANNEL)
            left_motor_inverted = config.getboolean(LEFT_MOTOR_SECTION, INVERTED)
            if (left_motor_channel):
                left_motor = Victor(left_motor_channel)
                if (left_motor):
                    left_motor.setInverted(left_motor_inverted)
                    self._left_motor=left_motor

        if (config.getboolean(RIGHT_MOTOR_SECTION, ENABLED)):
            right_motor_channel = config.getint(RIGHT_MOTOR_SECTION, CHANNEL)
            right_motor_inverted = config.getboolean(RIGHT_MOTOR_SECTION, INVERTED)
            if (right_motor_channel):
                right_motor = Victor(right_motor_channel)
                if (right_motor):
                    right_motor.setInverted(right_motor_inverted)
                    self._right_motor=right_motor

        if (config.getboolean(ENCODER_SECTION, ENABLED)):
            encoder_a_channel = config.getint(ENCODER_SECTION, "A_CHANNEL")
            encoder_b_channel = config.getint(ENCODER_SECTION, "B_CHANNEL")
            encoder_inverted = config.getboolean(ENCODER_SECTION, INVERTED)
            encoder_type = config.getint(ENCODER_SECTION, "TYPE")
            if (encoder_a_channel and encoder_b_channel and encoder_type):
                self._encoder = Encoder(encoder_a_channel, encoder_b_channel, encoder_inverted, encoder_type)

    # components
        # 2 motors for arms
        # 1 motor winch
        # 2 encoders, one on winch, one on arm

    # commands
        # moveArm up and down
        # extendArm
        # get/reset encoders
