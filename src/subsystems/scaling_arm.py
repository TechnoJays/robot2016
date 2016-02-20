'''
Created on Feb 6, 2016

@author: tylerstrayer
'''
from wpilib.command.subsystem import Subsystem
from wpilib.encoder import Encoder
from wpilib.victor import Victor
from wpilib.robotdrive import RobotDrive
from wpilib.talon import Talon
import configparser
import os

class ScalingArm(Subsystem):
    
    left_motor_section = "LeftMotor"
    right_motor_section = "RightMotor"
    winch_motor_section = "WinchMotor"
    winch_encoder_section = "WinchEncoder"
    arm_encoder_section = "ArmEncoder"
    
    _robot = None
    _config = None
    _arm_drive = None
    
    _left_motor = None
    _right_motor = None
    _winch_motor = None
    
    _arm_encoder = None
    _arm_encoder_a_channel = None
    _arm_encoder_b_channel = None
    _arm_encoder_reversed = False
    _arm_encoder_type = None
    _arm_encoder_value = 0
    
    _winch_encoder = None
    _winch_encoder_a_channel = None
    _winch_encoder_b_channel = None
    _winch_encoder_reversed = False
    _winch_encoder_type = None
    _winch_encoder_value = 0
    
    _left_motor_channel = None
    _right_motor_channel = None
    _winch_motor_channel = None
    
    _left_motor_inverted = False
    _right_motor_inverted = False
    _winch_motor_inverted = False
    
    def __init__(self, robot, name=None, configfile = 'arm.ini'):
        self._robot = robot;
        self._config = configparser.ConfigParser()
        self._config.read(os.path.join(os.getcwd(), configfile))
        self._init_components()
        super().__init__(name = name)
    
    def initDefaultCommand(self):
        return Subsystem.initDefaultCommand(self)
        
    def move_arm(self, speed):
        if (self._arm_drive):
            self._arm_drive.drive(speed, 0)
    
    def extend_arm(self, speed):
        if (self._winch_motor):
            self._winch_motor.setSpeed(speed)
            
    def get_winch_encoder_value(self):
        if (self._winch_encoder):
            self._winch_encoder_value = self._winch_encoder.get()
        return self._winch_encoder_value
    
    def reset_winch_encoder_value(self):
        if (self._winch_encoder):
            self._winch_encoder.reset()
            self._winch_encoder_value = self._winch_encoder.get()
        return self._winch_encoder_value
    
    def get_arm_encoder_value(self):
        if (self._arm_encoder):
            self._arm_encoder_value = self._arm_encoder.get()
        return self._arm_encoder_value
    
    def reset_arm_encoder_value(self):
        if (self._arm_encoder):
            self._arm_encoder.reset()
            self._arm_encoder_value = self._arm_encoder.get()
        return self._arm_encoder_value
    
    def _init_components(self):
        if (self._config.getboolean(self.left_motor_section, "MOTOR_ENABLED")):
            self._left_motor_channel = self._config.getint(self.left_motor_section, "MOTOR_CHANNEL")
            self._left_motor_inverted = self._config.getboolean(self.left_motor_section, "MOTOR_INVERTED")
            if (self._left_motor_channel):
                self._left_motor = Victor(self._left_motor_channel)
                if (self._left_motor):
                    self._left_motor.setInverted(self._left_motor_inverted)
                    
        if (self._config.getboolean(self.right_motor_section, "MOTOR_ENABLED")):
            self._right_motor_channel = self._config.getint(self.right_motor_section, "MOTOR_CHANNEL")
            self._right_motor_inverted = self._config.getboolean(self.right_motor_section, "MOTOR_INVERTED")
            if (self._right_motor_channel):
                self._right_motor = Victor(self._right_motor_channel)
                if (self._right_motor):
                    self._right_motor.setInverted(self._right_motor_inverted)
            
        if (self._right_motor and self._left_motor):
            self._arm_drive = RobotDrive(self._left_motor, self._right_motor)
            self._arm_drive.setSafetyEnabled(False)
            
        if (self._config.getboolean(self.winch_motor_section, "MOTOR_ENABLED")):
            self._winch_motor_channel = self._config.getint(self.winch_motor_section, "MOTOR_CHANNEL")
            self._winch_motor_inverted = self._config.getboolean(self.winch_motor_section, "MOTOR_INVERTED")
            if (self._winch_motor_channel):
                self._winch_motor = Talon(self._winch_motor_channel)
                if (self._winch_motor):
                    self._winch_motor.setInverted(self._winch_motor_inverted)
            
        if (self._config.getboolean(self.arm_encoder_section, "ENCODER_ENABLED")):
            self._arm_encoder_a_channel = self._config.getint(self.arm_encoder_section, "ENCODER_A_CHANNEL")
            self._arm_encoder_b_channel = self._config.getint(self.arm_encoder_section, "ENCODER_B_CHANNEL")
            self._arm_encoder_reversed = self._config.getboolean(self.arm_encoder_section, "ENCODER_REVERSED")
            self._arm_encoder_type = self._config.getint(self.arm_encoder_section, "ENCODER_TYPE")
            if (self._arm_encoder_a_channel and self._arm_encoder_b_channel and self._arm_encoder_type):
                self._arm_encoder = Encoder(self._arm_encoder_a_channel, self._arm_encoder_b_channel, self._arm_encoder_reversed, self._arm_encoder_type)
            
        if (self._config.getboolean(self.winch_encoder_section, "ENCODER_ENABLED")):
            self._winch_encoder_a_channel = self._config.getint(self.winch_encoder_section, "ENCODER_A_CHANNEL")
            self._winch_encoder_b_channel = self._config.getint(self.winch_encoder_section, "ENCODER_B_CHANNEL")
            self._winch_encoder_reversed = self._config.getboolean(self.winch_encoder_section, "ENCODER_REVERSED")
            self._winch_encoder_type = self._config.getint(self.winch_encoder_section, "ENCODER_TYPE")
            if (self._winch_encoder_a_channel and self._winch_encoder_b_channel and self._winch_encoder_type):
                self._winch_encoder = Encoder(self._winch_encoder_a_channel, self._winch_encoder_b_channel, self._winch_encoder_reversed, self._winch_encoder_type)
        
    # components
        # 2 motors for arms
        # 1 motor winch
        # 2 encoders, one on winch, one on arm
    
    # commands
        # moveArm up and down
        # extendArm 
        # get/reset encoders