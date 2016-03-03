'''
Created on Feb 20, 2016
Autonomous mode command groups need to be created and calibrated
Autonomous mode configured vias smartdashboard
// Autonomous init method should rest gyro to 0 before performing any actions
@author: james
'''

from wpilib.command import CommandGroup
from wpilib.smartdashboard import SmartDashboard
import configparser
from commands import lower_arm_to_count, turn_degrees, feed_ball_out,\
    drive_encoder_counts, extend_hook_to_count, turn_degrees_absolute
from math import sqrt

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
    
    _feeder_section = "Feeder"
    _feeder_speed = None
    _feed_time = None
    
    _arm_section = "Arm"
    _lower_bound = None
    _lower_speed = None
    
    _hook_section = "Hook"
    _extend_speed = None
    _raise_stop_count = None
    
    _starting_obstacle = None
    _target_obstacle = None
    _return_obstacle = None
    _obstacle_offset = None
    _angle = None
    _target_point = None
    _shoot_point = None
    _lane_width = None
    _direction = None
    _hypotenuse = None
    
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
        
        self._get_match_configuration()
        self._set_direction()
            
        self._obstacle_offset = abs(self._target_obstacle - self._starting_obstacle)
        
        self.robot.drivetrain.reset_gyro_angle()
        
        self.add_approach_commands()
        self.add_cross_commands()
        self.add_score_commands()
        self.add_return_commands()

    def _get_match_configuration(self):
        self._starting_obstacle = SmartDashboard.getNumber("Starting Obstacle")
        self._target_obstacle = SmartDashboard.getNumber("Target Obstacle")
        self._return_obstacle = SmartDashboard.getNumber("Return Obstacle")

    def _set_direction(self):
        if (self._target_obstacle > self._starting_obstacle):
            self._direction = 1
        elif (self._target_obstacle < self._starting_obstacle):
            self._direction = -1
        elif (self._target_obstacle == self._starting_obstacle):
            self._direction = 0

    def add_approach_commands(self):
        # lower arm
        self._approach_commands.addParallel(lower_arm_to_count.LowerArm(self._robot, self._lowered_bound, self._lower_speed))
        # extend hook
        self._approach_commands.addParallel(extend_hook_to_count.ExtendHookToCount(self._robot, self._extend_speed, self._raise_stop_count))

        if (self._obstacle_offset != 0):
            # turn toward target obstacle
            right_angle = 90 * self._direction
            self._approach_commands.addSequential(turn_degrees.TurnDegrees(self._robot, right_angle, self._auto_speed, self._drivetrain_threshold, self._drivetrain_ramp_threshold))
            # drive toward target obstacle
            alignment_drive = self._obstacle_offset * self._lane_width
            self._approach_commands.addSequential(drive_encoder_counts.DriveEncoderCounts(self._robot, alignment_drive, self._auto_speed, self._drivetrain_threshold, self._drivetrain_ramp_threshold))
            # turn to face obstacle
            right_angle = right_angle * -1
            self._approach_commands.addSequential(turn_degrees.TurnDegrees(self._robot, right_angle, self._auto_speed, self._drivetrain_threshold, self._drivetrain_ramp_threshold))
        
        # drive to obstacle line
        self._approach_commands.addSequential(drive_encoder_counts.DriveEncoderCounts(self._robot, self._distance_to_obstacle, self._auto_speed, self._drivetrain_threshold, self._drivetrain_ramp_threshold))   
        self.addSequential(self._approach_commands)
            
    def add_cross_commands(self):
        # cross the obstacle
        self._cross_commands.addSequential(drive_encoder_counts.DriveEncoderCounts(self._robot, self._target_obstacle, self._auto_speed, self._drivetrain_threshold, self._drivetrain_ramp_threshold))
        # re-center
        self._cross_commands.addSequential(turn_degrees_absolute.TurnDegreesAbsolute(self._robot, 0, self._speed, self._drivetrain_threshold, self._drivetrain_ramp_threshold))
        self.addSequential(self._cross_commands)
        
    def add_score_commands(self):
        # calculate angle of hyp/adj
        self._angle = self.math.degrees(self.math.atan(self._target_point / self._lane_width))
        # calculate length of hyp
        self._hypotenuse = sqrt((self._target_point ** 2) + (self._lane_width ** 2))
        
        if (self._target_obstacle == 1 or self._target_obstacle == 4):
            # turn to the right at [angle]
            self._score_commands.addSequential(turn_degrees.TurnDegrees(self._robot, self._angle, self._auto_speed, self._drivetrain_threshold, self._drivetrain_ramp_threshold))
            # drive to the target point along hyp
            self._score_commands.addSequential(drive_encoder_counts.DriveEncoderCounts(self._robot, self._hypotenuse, self._auto_speed, self._drivetrain_threshold, self._drivetrain_ramp_threshold))
            # vvvvv 45 is the angle of the goal relative to the back wall
            if (self._target_obstacle == 1):
                # turned [angle] toward goal, turn remainder of 45
                self._score_commands.addSequential(turn_degrees.TurnDegrees(self._robot, (45 - self._angle), self._auto_speed, self._drivetrain_threshold, self._drivetrain_ramp_threshold))
            elif (self._target_obstacle == 4):
                # turned away from goal by [angle], undo that turn then turn another -45 to face goal
                self._score_commands.addSequential(turn_degrees.TurnDegrees(self._robot, ((self._angle * -1) - 45), self._auto_speed, self._drivetrain_threshold, self._drivetrain_ramp_threshold))
        elif (self._target_obstacle == 2 or self._target_obstacle == 5):
            # drive to the target point along adj
            self._score_commands.addSequential(drive_encoder_counts.DriveEncoderCounts(self._robot, self._target_point, self._auto_speed, self._drivetrain_threshold, self._drivetrain_ramp_threshold))
            if (self._target_obstacle == 2):
                # turn to face goal
                self._score_commands.addSequential(turn_degrees.TurnDegrees(self._robot, 45, self._auto_speed, self._drivetrain_threshold, self._drivetrain_ramp_threshold))
            elif (self._target_obstacle == 5):
                # turn to face goal
                self._score_commands.addSequential(turn_degrees.TurnDegrees(self._robot, -45, self._auto_speed, self._drivetrain_threshold, self._drivetrain_ramp_threshold))
        elif (self._target_obstacle == 3):
            # turn to -[angle]
            self._score_commands.addSequential(turn_degrees.TurnDegrees(self._robot, (self._angle * -1), self._auto_speed, self._drivetrain_threshold, self._drivetrain_ramp_threshold))
            # drive to the target point along hyp
            self._score_commands.addSequential(drive_encoder_counts.DriveEncoderCounts(self._robot, self._hypotenuse, self._auto_speed, self._drivetrain_threshold, self._drivetrain_ramp_threshold))
            # turn to face goal
            self._score_commands.addSequential(turn_degrees.TurnDegrees(self._robot, (self._angle + 45), self._auto_speed, self._drivetrain_threshold, self._drivetrain_ramp_threshold))
        # drive toward goal
        self._score_commands.addSequential(drive_encoder_counts.DriveEncoderCounts(self._robot, self._shoot_point, self._auto_speed, self._drivetrain_threshold, self._drivetrain_ramp_threshold))
        # shoot
        self._score_commands.addSequential(feed_ball_out.FeedBallOut(self._robot, self._feeder_speed, self._feed_time))
        self.addSequential(self._score_commands)
        
    def add_return_commands(self):
        # turn around
        if (self._target_obstacle == 1 or self._target_obstacle == 2 or self._target_obstacle == 3):
            # turn to face obstacles
            self._return_commands.addSequential(turn_degrees.TurnDegrees(self._robot, 135, self._auto_speed, self._drivetrain_threshold, self._drivetrain_ramp_threshold))
        elif (self._target_obstacle == 4 or self._target_obstacle == 5):
            # turn to face obstaclces
            self._return_commands.addSequential(turn_degrees.TurnDegrees(self._robot, -135, self._auto_speed, self._drivetrain_threshold, self._drivetrain_ramp_threshold))
        # drive to obstacles
        self._return_commands.addSequential(drive_encoder_counts.DriveEncoderCounts(self._robot, self._target_point, self._auto_speed, self._drivetrain_threshold, self._drivetrain_ramp_threshold))
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
        self._target_obstacle = self._config.getint(self._drivetrain_section, "CROSS_OBSTACLE")
        self._degrees_center = self._config.getint(self._drivetrain_section, "DEGREES_TARGET")
        self._distance_to_turn = self._config.getint(self._drivetrain_section, "DISTANCE_TO_TURN")
        self._angle = (self._lane_width ** 2) + (self._hyp)
        self._target_point = self._config.getint(self._drivetrain_section, "DISTANCE_TO_SCORE")
        self._degrees_to_defense = self._config.getint(self._drivetrain_section, "DEGREES_TO_DEFENSE")
        
        # feeder
        self._feeder_speed = self._config.getfloat(self._feeder_section, "FEEDER_SPEED")
        self._feed_time = self._config.getint(self._feeder_section, "FEED_TIME")
        
        # arm
        self._lower_bound = self._config.getint(self._feeder_section, "LOWER_BOUND")
        self._lower_speed = self._config.getfloat(self._feeder_section, "LOWER_SPEED")
        
        
        
        
        
        
        
        
        
        
        

        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        