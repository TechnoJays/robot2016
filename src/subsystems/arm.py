'''
Created on Feb 6, 2016

@author: tylerstrayer
'''
from wpilib.command.subsystem import Subsystem
from wpilib.encoder import Encoder
from wpilib.victor import Victor
from wpilib.robotdrive import RobotDrive
from commands.move_arm_analog import MoveArmAnalog
from wpilib.smartdashboard import SmartDashboard

import configparser
import os

class Arm(Subsystem):

    _robot = None
    _config_file = None
    _arm_drive = None
    _encoder = None
    _encoder_value = 0

    def __init__(self, robot, name=None, configfile = 'configs/subsystems.ini'):
        self._robot = robot;
        self._config_file = configfile
        self._init_components()
        self._update_smartdashboard(0.0)
        super().__init__(name = name)

    def initDefaultCommand(self):
        self.setDefaultCommand(MoveArmAnalog(self._robot, 50))

    def move_arm(self, speed):
        if (self._arm_drive):
            self._arm_drive.drive(speed, 0)
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
        config.read(os.path.join(os.getcwd(), self._config_file))

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

        if (config.getboolean(RIGHT_MOTOR_SECTION, ENABLED)):
            right_motor_channel = config.getint(RIGHT_MOTOR_SECTION, CHANNEL)
            right_motor_inverted = config.getboolean(RIGHT_MOTOR_SECTION, INVERTED)
            if (right_motor_channel):
                right_motor = Victor(right_motor_channel)
                if (right_motor):
                    right_motor.setInverted(right_motor_inverted)

        if (right_motor and left_motor):
            self._arm_drive = RobotDrive(left_motor, right_motor)
            self._arm_drive.setSafetyEnabled(False)

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
