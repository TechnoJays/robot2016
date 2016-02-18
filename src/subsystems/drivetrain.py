'''
Created on Jan 23, 2016

@author: Ty Strayer
'''

import configparser
import os

from wpilib.command.subsystem import Subsystem
from wpilib.encoder import Encoder
from wpilib.robotdrive import RobotDrive
from wpilib.talon import Talon
from wpilib.analoggyro import AnalogGyro

from commands.tank_drive import TankDrive


class Drivetrain(Subsystem):
    '''
    classdocs
    '''
    # 2 Talon controllers
    # 

    # Config file section names
    left_motor_section = "LeftMotor"
    right_motor_section = "RightMotor"
    general_section = "General"
    encoder_section = "Encoder"
    gyro_section = "Gyro"

    # General config parameters
    _max_speed = 0

    _robot = None
    _config = None

    _left_motor = None
    _right_motor = None
    _robot_drive = None
    
    _encoder = None
    _encoder_a_channel = None
    _encoder_b_channel = None
    _encoder_reversed = None
    _encoder_type = None
    _encoder_count = 0
    
    _gyro = None
    _gyro_angle = None
    _gyro_channel = None
    _gyro_sensitivity = None

    def __init__(self, robot, name = None, configfile = 'drivetrain.ini'):
        self._robot = robot;
        self._config = configparser.ConfigParser()
        self._config.read(os.path.join(os.getcwd(), configfile))
        self._load_general_config()
        self._init_components()
        super().__init__(name = name)

    def initDefaultCommand(self):
        self.setDefaultCommand(TankDrive(self._robot, self._robot._oi))

    def tank_drive(self, leftSpeed, rightSpeed):
        left = leftSpeed * self._max_speed
        right = rightSpeed * self._max_speed
        self._robot_drive.tankDrive(left, right, False)

    def _load_general_config(self):
        self._max_speed = self._config.getfloat('General', "MAX_SPEED")
        
    def get_encoder_value(self):
        if(self._encoder):
            self._encoder_count = self._encoder.get()
        return self._encoder_count
    
    def reset_encoder_value(self):
        if(self._encoder):
            self._encoder_count = 0
        return self._encoder_count
    
    def get_gyro_angle(self):
        if (self._gyro):
            self._gyro_angle = self._gyro.getAngle()
        return self._gyro_angle
    
    def reset_gyro_angle(self):
        if (self._gyro):
            self._gyro.reset()
            self._gyro_angle = self._gyro.getAngle()
        return self._gyro_angle
    
    def arcade_drive(self, linearDistance, turnAngle):
        if(self._robot_drive):
            self._robot_drive.arcadeDrive(linearDistance, turnAngle)
        
    def _init_components(self):
        if(self._config.getboolean(Drivetrain.encoder_section, "ENCODER_ENABLED")):
            self._encoder_a_channel = self._config.getint(self.encoder_section, "ENCODER_A_CHANNEL")
            self._encoder_b_channel = self._config.getint(self.encoder_section, "ENCODER_B_CHANNEL")
            self._encoder_reversed = self._config.getboolean(self.encoder_section, "ENCODER_REVERSED")
            self._encoder_type = self._config.getint(self.encoder_section, "ENCODER_TYPE")
            if(self._encoder_a_channel and self._encoder_b_channel and self._encoder_reversed and self._encoder_type):
                self._encoder = Encoder(self._encoder_a_channel, self._encoder_b_channel, self._encoder_reversed, self._encoder_type)
        
        if(self._config.getboolean(Drivetrain.gyro_section, "GYRO_ENABLED")):
            self._gyro_channel = self._config.getint(self.gyro_section, "GYRO_CHANNEL")
            self._gyro_sensitivity = self._config.getfloat(self.gyro_section, "GYRO_SENSITIVITY")
            if (self._gyro_channel):
                self._gyro = AnalogGyro(self._gyro_channel)
                if (self._gyro and self._gyro_sensitivity):
                    self._gyro.setSensitivity(self._gyro_sensitivity)
                
        if(self._config.getboolean(Drivetrain.left_motor_section, "MOTOR_ENABLED")):
            self._left_motor = Talon(self._config.getint(self.left_motor_section, "MOTOR_CHANNEL"))

        if(self._config.getboolean(Drivetrain.right_motor_section, "MOTOR_ENABLED")):
            self._right_motor = Talon(self._config.getint(self.right_motor_section, "MOTOR_CHANNEL"))

        if(self._left_motor and self._right_motor):
            self._robot_drive = RobotDrive(self._left_motor, self._right_motor)
            self._robot_drive.setSafetyEnabled(False)
            self._robot_drive.setInvertedMotor(RobotDrive.MotorType.kRearLeft,
                                               self._config.getboolean(Drivetrain.left_motor_section,
                                                                       "MOTOR_INVERTED"))
            self._robot_drive.setInvertedMotor(RobotDrive.MotorType.kRearRight,
                                               self._config.getboolean(Drivetrain.right_motor_section,
                                                                       "MOTOR_INVERTED"))
