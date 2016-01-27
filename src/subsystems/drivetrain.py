'''
Created on Jan 23, 2016

@author: Ty Strayer
'''
from configparser import ConfigParser

from wpilib.command.subsystem import Subsystem
from wpilib.robotdrive import RobotDrive
from wpilib.talon import Talon

from commands.tank_drive import TankDrive


class Drivetrain(Subsystem):
    '''
    classdocs
    '''
    # 2 Talon controllers
    
    # Config file section names
    left_motor_section = "LeftMotor"
    right_motor_section = "RightMotor"
    general_section = "General"
    
    # General config parameters
    _max_speed = 0
    
    _robot = None
    _config = None
    
    _left_motor = None
    _right_motor = None
    _robot_drive = None
    
    
    def __init__(self, robot, name = None):
        super().__init__(name = name)
        self._robot = robot;
        self._config = ConfigParser.read("../configs/drivetrain.ini")
        self._load_general_config()

    def initDefaultCommand(self):
        self.setDefaultCommand(TankDrive(self.robot, self.robot._oi))
    
    def tankDrive(self, leftSpeed, rightSpeed):
        left = leftSpeed * self._max_speed
        right = rightSpeed * self._max_speed
        
        self._robot_drive.tankDrive(left, right, False)
        
    def _load_general_config(self):
        self._max_speed = self._config.getint(self.general_section, "MAX_SPEED")
    
    def _init_components(self):
        if(self._config.getboolean(Drivetrain.left_motor_section, "MOTOR_ENABLED")):
            _left_motor = Talon(self._config.getint(self.left_motor_section, "MOTOR_CHANNEL"))
            
        if(self._config.getboolean(Drivetrain.right_motor_section, "MOTOR_ENABLED")):
            _right_motor = Talon(self._config.getint(self.right_motor_section, "MOTOR_CHANNEL"))
            
        if(_left_motor and _right_motor):
            self._robot_drive = RobotDrive(self._left_motor, self._right_motor)
            self._robot_drive.setSafetyEnabled(False)
            self._robot_drive.setInvertedMotor(RobotDrive.MotorType.kRearLeft,
                                               self._config.getboolean(Drivetrain.left_motor_section,
                                                                       "MOTOR_INVERTED"))
            self._robot_drive.setInvertedMotor(RobotDrive.MotorType.kRearRight,
                                               self._config.getboolean(Drivetrain.right_motor_section,
                                                                       "MOTOR_INVERTED"))
            