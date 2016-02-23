'''
Created on Feb 20, 2016

@author: james
'''

from wpilib.command import CommandGroup
import configparser
from commands import lower_arm_to_count, turn_degrees, feed_ball_out,\
    drive_encoder_counts, extend_hook_to_count, turn_degrees_absolute

class AutoCommandGroup(CommandGroup):
    '''
    classdocs
    '''
    _robot = None
    _config = None
    
    _drivetrain_section = "Drivetrain"
    _distance_to_obstacle = None
    _auto_speed = None
    _drivetrain_threshold = None
    _drivetrain_ramp_threshold = None
    _cross_obstacle = None
    _degrees_center = None
    _distance_to_turn = None
    _degrees_turn = None
    _distance_to_score = None
    _degrees_to_defense = None
    
    _feeder_section = "Feeder"
    _feeder_speed = None
    _feed_time = None
    
    _arm_section = "Arm"
    _lower_bound = None
    _lower_speed = None
    
    _hook_section = "Hook"
    _extend_speed = None
    _raise_stop_count = None
    
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
    _turn_around = 180
    
    # command groups
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
        self._alignment_drive = self._obstacle_offset * self._lane_width
        self._right_angle = self._right_angle * self._direction
        
        self.add_approach_commands()
        self.add_cross_commands()
        self.add_score_commands()
        self.add_return_commands()

#command groups:
    #approach: lower arm, extend hook, drive
        #if !0 turn, drive, turn
    #cross: drive (gyro or encoder?), re-center
    #score: drive, turn, drive, shoot
    #return: turn, drive, turn, drive

    def add_approach_commands(self):
        # lower arm
        self._approach_commands.addParallel(lower_arm_to_count.LowerArm(self._robot, self._lowered_bound, self._lower_speed))
        # extend hook
        self._approach_commands.addParallel(extend_hook_to_count.ExtendHookToCount(self._robot, self._extend_speed, self._raise_stop_count))

        if (self._obstacle_offset != 0):
            # turn toward target obstacle
            self._approach_commands.addSequential(turn_degrees.TurnDegrees(self._robot, self._right_angle, self._auto_speed, self._drivetrain_threshold, self._drivetrain_ramp_threshold))
            # drive toward target obstacle
            self._approach_commands.addSequential(drive_encoder_counts.DriveEncoderCounts(self._robot, self._alignment_drive, self._auto_speed, self._drivetrain_threshold, self._drivetrain_ramp_threshold))
            self._right_angle = self._right_angle * -1
            # turn to face obstacle
            self._approach_commands.addSequential(turn_degrees.TurnDegrees(self._robot, self._right_angle, self._auto_speed, self._drivetrain_threshold, self._drivetrain_ramp_threshold))
        
        # drive to obstacle line
        self._approach_commands.addSequential(drive_encoder_counts.DriveEncoderCounts(self._robot, self._distance_to_obstacle, self._auto_speed, self._drivetrain_threshold, self._drivetrain_ramp_threshold))   
        self.addSequential(self._approach_commands)
            
    def add_cross_commands(self):
        # cross the obstacle
        self._cross_commands.addSequential(drive_encoder_counts.DriveEncoderCounts(self._robot, self._cross_obstacle, self._auto_speed, self._drivetrain_threshold, self._drivetrain_ramp_threshold))
        # re-center
        self._cross_commands.addSequential(turn_degrees_absolute.TurnDegreesAbsolute(self._robot, self._degrees_center, self._speed, self._drivetrain_threshold, self._drivetrain_ramp_threshold))
        self.addSequential(self._cross_commands)
        
    def add_score_commands(self):
        # drive to turning point
        self._score_commands.addSequential(drive_encoder_counts.DriveEncoderCounts(self._robot, self._distance_to_turn, self._auto_speed, self._drivetrain_threshold, self._drivetrain_ramp_threshold))
        # turn toward goal
        self._score_commands.addSequential(turn_degrees_absolute.TurnDegreesAbsolute(self._robot, self._degrees_turn, self._auto_speed, self._drivetrain_threshold, self._drivetrain_ramp_threshold))
        # drive toward goal
        self._score_commands.addSequential(drive_encoder_counts.DriveEncoderCounts(self._robot, self._distance_to_score, self._auto_speed, self._drivetrain_threshold, self._drivetrain_ramp_threshold))
        # shoot!
        self._score_commands.addSequential(feed_ball_out.FeedBallOut(self._robot, self._feeder_speed, self._feed_time))
        self.addSequential(self._score_commands)
        
    def add_return_commands(self):
        # turn around
        self._return_commands.addSequential(turn_degrees.TurnDegrees(self._robot, self._turn_around, self._auto_speed, self._drivetrain_threshold, self._drivetrain_ramp_threshold))
        # drive back to turning point
        self._return_commands.addSequential(drive_encoder_counts.DriveEncoderCounts(self._robot, self._distance_to_score, self._auto_speed, self._drivetrain_threshold, self._drivetrain_ramp_threshold))
        # turn to defenses
        self._return_commands.addSequential(turn_degrees_absolute.TurnDegreesAbsolute(self._robot, self._degrees_to_defense, self._auto_speed, self._drivetrain_threshold, self._drivetrain_ramp_threshold))
        # drive to defenses
        self._return_commands.addSequential(drive_encoder_counts.DriveEncoderCounts(self._robot, self._distance_to_turn, self._auto_speed, self._drivetrain_threshold, self._drivetrain_ramp_threshold))
        self.addSequential(self._return_commands)
        
    def _init_commands(self):
        # hook
        self._extend_speed = self._config.getfloat(self._hook_section, "EXTEND_SPEED")
        self._raise_stop_count = self._config.getint(self._hook_section, "RAISE_STOP_COUNT")
        
        # drivetrain
        self._distance_to_obstacle = self._config.getint(self._drivetrain_section, "DISTANCE_TO_OBSTACLE")
        self._auto_speed = self._config.getint(self._drivetrain_section, "SPEED")
        self._drivetrain_threshold = self._config.getint(self._drivetrain_section, "THRESHOLD")
        self._drivetrain_ramp_threshold = self._config.getint(self._drivetrain_section, "RAMP_THRESHOLD")
        self._cross_obstacle = self._config.getint(self._drivetrain_section, "CROSS_OBSTACLE")
        self._degrees_center = self._config.getint(self._drivetrain_section, "DEGREES_TARGET")
        self._distance_to_turn = self._config.getint(self._drivetrain_section, "DISTANCE_TO_TURN")
        self._degrees_turn = self._config.getint(self._drivetrain_section, "DEGREES_TURN")
        self._distance_to_score = self._config.getint(self._drivetrain_section, "DISTANCE_TO_SCORE")
        self._degrees_to_defense = self._config.getint(self._drivetrain_section, "DEGREES_TO_DEFENSE")
        
        # feeder
        self._feeder_speed = self._config.getfloat(self._feeder_section, "FEEDER_SPEED")
        self._feed_time = self._config.getint(self._feeder_section, "FEED_TIME")
        
        # arm
        self._lower_bound = self._config.getint(self._feeder_section, "LOWER_BOUND")
        self._lower_speed = self._config.getfloat(self._feeder_section, "LOWER_SPEED")
        
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
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        