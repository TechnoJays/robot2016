'''
Created on Feb 6, 2016

@author: tylerstrayer
'''
from wpilib.command.subsystem import Subsystem
from wpilib.talon import Talon
from wpilib.digitalinput import DigitalInput
import configparser
import os
from commands.feed_ball_out import FeedBallOut
from commands.feed_ball_analog import FeedBallAnalog

class Feeder(Subsystem):
    
    motor_section = "Motor"
    switch_section = "Switch"
    
    _motor_channel = None
    _switch_channel = None
    _motor_inverted = None
    
    _robot = None
    _config = None
    _motor = None
    _switch = None
    _has_ball = False
    
    def __init__(self, robot, name = None, configfile = 'feeder.ini'):
        self._robot = robot;
        self._config = configparser.ConfigParser()
        self._config.read(os.path.join(os.getcwd(), configfile))
        self._init_components()
        super().__init__(name = name)
    
    def initDefaultCommand(self):
        self.setDefaultCommand(FeedBallAnalog(self._robot))
    
    def spinFeeder(self, speed):
        """Spins the feeder in the given direction at a speed represented as a float"""
        if (self._motor):
            self._motor.set(speed)
    
    def hasBall(self):
        if (self._switch):
            self._has_ball = self._switch.get()
        return self._has_ball
    
    def _init_components(self):
        if (self._config.getboolean(Feeder.motor_section, "MOTOR_ENABLED")):
            self._motor_channel = self._config.getint(self.motor_section, "MOTOR_CHANNEL")
            self._motor_inverted = self._config.getboolean(self.motor_section, "MOTOR_INVERTED")
        
        if (self._motor_channel):
            self._motor = Talon(self._motor_channel)
            if (self._motor_inverted):
                self._motor.setInverted(self._motor_inverted)
            
        if (self._config.getboolean(Feeder.switch_section, "SWITCH_ENABLED")):
            self._switch_channel = self._config.getint(self.switch_section, "SWITCH_CHANNEL")
            
        if (self._switch_channel):
            self._switch = DigitalInput(self._switch_channel)