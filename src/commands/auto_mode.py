'''
Created on Feb 20, 2016

@author: james
'''

from wpilib.command import CommandGroup
import os
import configparser
from commands import lower_arm_to_count, drive_time, turn_degrees, feed_ball_out,\
    drive_encoder_counts

class AutoCommandGroup(CommandGroup):
    '''
    classdocs
    '''
    _robot = None
    _config = None
    
    _drivetrain_section = "Drivetrain"
    _half_distance_to_obstacle = None
    _auto_speed = None
    _drivetrain_threshold = None
    _drivetrain_ramp_threshold = None
    
    _auto_feeder_section = "Feeder"
    
    _auto_arm_section = "Arm"
    
    _auto_hook_section = "Hook"
    
    _obstacle_target = None
    _starting_position = None
    _obstacle_offset = None
    _alignment_drive = None
    _lane_width = None
    _right_angle = 90
    _direction = None

    def __init__(self, robot, start_position, target_obstacle, configfile = "configs/auto.ini"):
        self._robot = robot
        self._config = configparser.ConfigParser()
        self._config.read(os.path.join(os.getcwd(), configfile))
        self._init_commands()
        
        if (self._obstacle_target > self._starting_position):
            self._direction = 1
        elif (self._obstacle_target < self._starting_position):
            self._direction = -1
        elif (self._obstacle_target == self._starting_position):
            self._direction = 0
            
        self._obstacle_offset = abs(self._obstacle_target - self._starting_position)
        
        self.execute_commands()

    def execute_commands(self):
        if (self):
            self.addParallel(lower_arm_to_count.LowerArm(self._robot, self._arm_lowered_bound, self._arm_lower_speed, None, self._arm_timeout))
            self.addSequential(drive_encoder_counts.DriveEncoderCounts(self._robot, self._half_distance_to_obstacle, self._auto_speed, self._drivetrain_threshold, self._drivetrain_ramp_threshold))
            if (self._obstacle_offset != 0):
                self._alignment_drive = self._obstacle_offset * self._lane_width
                self._right_angle = self._right_angle * self._direction
                self.addSequential(turn_degrees.TurnDegrees(self._robot, self._right_angle, self._auto_speed, self._drivetrain_threshold, self._drivetrain_ramp_threshold))
                self.addSequential(drive_encoder_counts.DriveEncoderCounts(self._robot, self._alignment_drive, self._auto_speed, self._drivetrain_threshold, self._drivetrain_ramp_threshold))
                self._right_angle = self._right_angle * -1
                self.addSequential(turn_degrees.TurnDegrees(self._robot, self._right_angle, self._auto_speed, self._drivetrain_threshold, self._drivetrain_ramp_threshold))
                self.addSequential(drive_encoder_counts.DriveEncoderCounts(self._robot, self._half_distance_to_obstacle, self._auto_speed, self._drivetrain_threshold, self._drivetrain_ramp_threshold))
            elif (self._obstacle_offset == 0):
                self.addSequential(drive_encoder_counts.DriveEncoderCounts(self._robot, self._half_distance_to_obstacle, self._auto_speed, self._drivetrain_threshold, self._drivetrain_ramp_threshold))
            
    def _init_commands(self):
        self._half_distance_to_obstacle = self._config.getint(self._drivetrain_section, "HALF_DISTANCE_TO_OBSTACLE")
        self._auto_speed = self._config.getint(self._drivetrain_section, "SPEED")
        self._drivetrain_threshold = self._config.getint(self._drivetrain_section, "THRESHOLD")
        self._drivetrain_ramp_threshold = self._config.getint(self._drivetrain_section, "RAMP_THRESHOLD")
        self._lane_width = self._config.getint(self._drivetrain_section, "LANE_WIDTH")
        
        #Parallel
        # Move arm down
        # Move robot forward
        # Sequential
        # Move robot forward
        # Turn x degrees
        # Move robot forward
        # Turn x degrees
        # Shoot
        #
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        