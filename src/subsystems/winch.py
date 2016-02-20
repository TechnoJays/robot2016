'''
Created on Feb 19, 2016

@author: james
'''
from wpilib.command.subsystem import Subsystem
from wpilib.encoder import Encoder
from wpilib.talon import Talon
import configparser
import os

class Winch(Subsystem):

    _robot = None
    _config_file = None
    
    _motor = None
    
    _encoder = None
    _encoder_value = 0


    def __init__(self, robot, name=None, configfile = 'winch.ini'):
        self._robot = robot;
        self._config_file = configfile
        self._init_components()
        super().__init__(name = name)
        
    def extend_arm(self, speed):
        if (self._motor):
            self._motor.setSpeed(speed)
        
    def get_encoder_value(self):
        if (self._encoder):
            self._encoder_value = self._encoder.get()
        return self._encoder_value
    
    def reset_encoder_value(self):
        if (self._encoder):
            self._encoder.reset()
            self._encoder_value = self._encoder.get()
        return self._encoder_value
    
    def _init_components(self):
        
        config = configparser.ConfigParser()
        config.read(os.path.join(os.getcwd(), self._config_file))
    
        MOTOR_SECTION = "Motor"
        ENCODER_SECTION = "Encoder"
        ENABLED = "ENABLED"
        CHANNEL = "CHANNEL"
        INVERTED = "INVERTED"
        
        if (self._config.getboolean(MOTOR_SECTION, ENABLED)):
            motor_channel = self._config.getint(MOTOR_SECTION, CHANNEL)
            motor_inverted = self._config.getboolean(MOTOR_SECTION, INVERTED)
            if (motor_channel):
                self._motor = Talon(motor_channel)
                if (self._motor):
                    self._motor.setInverted(motor_inverted)
                    
        if (config.getboolean(ENCODER_SECTION, ENABLED)):
            encoder_a_channel = config.getint(ENCODER_SECTION, "A_CHANNEL")
            encoder_b_channel = config.getint(ENCODER_SECTION, "B_CHANNEL")
            encoder_inverted = config.getboolean(ENCODER_SECTION, INVERTED)
            encoder_type = config.getint(ENCODER_SECTION, "TYPE")
            if (encoder_a_channel and encoder_b_channel and encoder_type):
                self._encoder = Encoder(encoder_a_channel, encoder_b_channel, encoder_inverted, encoder_type)
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    