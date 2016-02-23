'''
Created on Feb 19, 2016

@author: james
'''
from wpilib.command.subsystem import Subsystem
from wpilib.encoder import Encoder
from wpilib.talon import Talon
from commands.move_hook_analog import MoveHookAnalog
from wpilib.smartdashboard import SmartDashboard

import configparser
import os
from wpilib.victorsp import VictorSP


class Hook(Subsystem):

    _robot = None
    _subsystem_config = None
    _motor = None
    _encoder = None
    _encoder_value = 0


    def __init__(self, robot, name=None, configfile = '/home/lvuser/configs/subsystems.ini'):
        self._robot = robot;
        self._subsystem_config = configfile
        self._init_components()
        self._update_smartdashboard(0.0)
        super().__init__(name = name)

    def initDefaultCommand(self):
        # Make it not a magic number
        self.setDefaultCommand(MoveHookAnalog(self._robot, 50))

    def move_hook(self, speed):
        if (self._motor):
            self._motor.setSpeed(speed)
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
        SmartDashboard.putNumber("Hook Encoder", self._encoder_value)
        SmartDashboard.putNumber("Hook Speed", speed)

    def _init_components(self):

        config = configparser.ConfigParser()
        config.read(os.path.join(os.getcwd(), self._subsystem_config))

        MOTOR_SECTION = "HookMotor"
        ENCODER_SECTION = "HookEncoder"
        ENABLED = "ENABLED"
        CHANNEL = "CHANNEL"
        INVERTED = "INVERTED"

        if (config.getboolean(MOTOR_SECTION, ENABLED)):
            motor_channel = config.getint(MOTOR_SECTION, CHANNEL)
            motor_inverted = config.getboolean(MOTOR_SECTION, INVERTED)
            if (motor_channel):
                self._motor = VictorSP(motor_channel)
                if (self._motor):
                    self._motor.setInverted(motor_inverted)

        if (config.getboolean(ENCODER_SECTION, ENABLED)):
            encoder_a_channel = config.getint(ENCODER_SECTION, "A_CHANNEL")
            encoder_b_channel = config.getint(ENCODER_SECTION, "B_CHANNEL")
            encoder_inverted = config.getboolean(ENCODER_SECTION, INVERTED)
            encoder_type = config.getint(ENCODER_SECTION, "TYPE")
            if (encoder_a_channel and encoder_b_channel and encoder_type):
                self._encoder = Encoder(encoder_a_channel, encoder_b_channel, encoder_inverted, encoder_type)
