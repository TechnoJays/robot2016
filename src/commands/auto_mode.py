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
    _distance_to_obstacle = None
    _distance_to_shooting_line = None
    _distance_to_shooting_position = None
    _auto_speed = None
    _drivetrain_threshold = None
    _drivetrain_ramp_threshold = None
    
    _auto_feeder_section = "Feeder"
    
    _auto_arm_section = "Arm"
    
    _auto_hook_section = "Hook"
    
    # determine which direction, if any, and how far to travel to obstacle
    _obstacle_target = None
    _starting_position = None
    _return_obstacle_target = None
    _obstacle_offset = None
    _alignment_drive = None
    _lane_width = None
    _right_angle = 90
    _direction = None
    _turn_to_goal = None
    _turn_back_to_obstacle = 180
    _approach_commands = CommandGroup()
    _cross_commands = CommandGroup()
    _score_commands = CommandGroup()
    _return_commands = CommandGroup()

    def __init__(self, robot, start_position, target_obstacle, configfile = "/home/lvuser/configs/auto.ini"):
        self._robot = robot
        self._config = configparser.ConfigParser()
        self._config.read(configfile)
        self._init_commands()
        
        if (self._obstacle_target > self._starting_position):
            self._direction = 1
        elif (self._obstacle_target < self._starting_position):
            self._direction = -1
        elif (self._obstacle_target == self._starting_position):
            self._direction = 0
            
        self._obstacle_offset = abs(self._obstacle_target - self._starting_position)
        
        self.add_commands()

#command groups:
    #approach: lower arm, extend hook, drive
        #if !0 turn, drive, turn
    #cross: drive (gyro or encoder?), re-center
    #score: drive, turn, drive, shoot
    #return: turn, drive, turn, drive

    def add_commands(self):
        self._init_alignment_drive = self._obstacle_offset * self._lane_width
        self._right_angle = self._right_angle * self._direction
        
        #todo extend hook slightly
        self._approach_commands.addParallel(lower_arm_to_count.LowerArm(self._robot, self._arm_lowered_bound, self._arm_lower_speed, None, self._arm_timeout))
        
        
        if (self._obstacle_offset != 0):
        
            # approach defense command group
            self._approach_commands.addSequential(turn_degrees.TurnDegrees(self._robot, self._right_angle, self._auto_speed, self._drivetrain_threshold, self._drivetrain_ramp_threshold))

            
            # main command group
            self.addSequential(drive_encoder_counts.DriveEncoderCounts(self._robot, self._alignment_drive, self._auto_speed, self._drivetrain_threshold, self._drivetrain_ramp_threshold))
            self._right_angle = self._right_angle * -1
            self.addSequential(turn_degrees.TurnDegrees(self._robot, self._right_angle, self._auto_speed, self._drivetrain_threshold, self._drivetrain_ramp_threshold))
            self.addSequential(drive_encoder_counts.DriveEncoderCounts(self._robot, self._distance_to_obstacle, self._auto_speed, self._drivetrain_threshold, self._drivetrain_ramp_threshold))
            # todo add DriveEncoderCounts over obstacle
            
        elif (self._obstacle_offset == 0):
            self._approach_commands.addSequential(lower_arm_to_count.LowerArm(self._robot, self._arm_lowered_bound, self._arm_lower_speed, None, self._arm_timeout))
            self._approach_commands.addSequential(drive_encoder_counts.DriveEncoderCounts(self._robot, self._distance_to_obstacle, self._auto_speed, self._drivetrain_threshold, self._drivetrain_ramp_threshold))
        
        self.addSequential(self._approach_commands)
        
        #todo correct direction based on gyro?
        #todo distance_to_shooting_line * (enum with pre-determined counts based on target obstacle?) OR "math that shit"
        self.addSequential(drive_encoder_counts.DriveEncoderCounts(self._robot, self._distance_to_shooting_line, self._auto_speed, self._drivetrain_threshold, self._drivetrain_ramp_threshold))
        #todo turn toward goal (enum with pre-determined angles based on target obstacle?) OR "math that shit"
        #todo self.addSequential(turn toward goal)
        self.addSequential(drive_encoder_counts.DriveEncoderCounts(self._robot, self._distance_to_shooting_position, self._auto_speed, self._drivetrain_threshold, self._drivetrain_ramp_threshold))
        # self.addSequential(feed_ball_out.FeedBallOut(self._robot))
        # self._turn_back_to_obstacle = self._turn_back_to_obstacle - ^ the angle used on line 78
        self.addSequential(turn_degrees.TurnDegrees(self._robot, self._turn_back_to_obstacle, self._auto_speed, self._drivetrain_threshold, self._drivetrain_ramp_threshold))
        self.addSequential(drive_encoder_counts.DriveEncoderCounts(self._robot, self._distance_to_obstacle, self._auto_speed, self._drivetrain_threshold, self._drivetrain_ramp_threshold))
            
    def _init_commands(self):
        self._distance_to_obstacle = self._config.getint(self._drivetrain_section, "DISTANCE_TO_OBSTACLE")
        self._auto_speed = self._config.getint(self._drivetrain_section, "SPEED")
        self._drivetrain_threshold = self._config.getint(self._drivetrain_section, "THRESHOLD")
        self._drivetrain_ramp_threshold = self._config.getint(self._drivetrain_section, "RAMP_THRESHOLD")
        self._lane_width = self._config.getint(self._drivetrain_section, "LANE_WIDTH")
        self._distance_to_shooting_line = self._config.getint(self._drivetrain_section, "DISTANCE_TO_SHOOTING_LINE")
        self._distance_to_shooting_position = self._config.getint(self._drivetrain_section, "DISTANCE_TO_SHOOTING_POSITION")
        
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
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        