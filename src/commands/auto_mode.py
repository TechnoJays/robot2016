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
from commands import lower_arm_to_count, turn_degrees, feed_ball_out, \
    drive_encoder_counts, extend_hook_to_count, turn_degrees_absolute
import math

class AutoCommandGroup(CommandGroup):
    '''
    classdocs
    '''
    _robot = None
    _config = None
    _default_timeout = 15

    _drivetrain_section = "Drivetrain"
    _auto_speed = None
    _drivetrain_threshold = None

    _feeder_section = "Feeder"
    _feeder_speed = None
    _feed_time = None

    _arm_section = "Arm"
    _lower_bound = None
    _lower_speed = None

    _hook_section = "Hook"
    _extend_speed = None
    _raise_stop_count = None

    _starting_obstacle = None # the obstacle we're starting in front of in autonomous mode
    _target_obstacle = None # the obstacle we want to traverse during autonomous mode
    _return_obstacle = None # the obstacle we want to end on during autonomous mode
    _obstacle_offset = None # distance in whole lane widths from starting obstacle to target obstacle
    _obstacle_direction = None # direction from starting obstacle to target obstacle
    _distance_to_obstacle = None # distance from starting line to obstacles, unneeded if crossing based on pitch gyro
    _target_point = None # point which we want to reach after traversing the target obstacle
    _shoot_point = None # point from which we want to shoot the ball, at foot of ramp
    _lane_width = None # distance to travel from the center of one obstacle to the center of another
    _cross_obstacle = None # distance to travel to traverse obstacle, unneeded if crossing based on pitch gyro

    # command groups
    _approach_commands = CommandGroup()
    _cross_commands = CommandGroup()
    _score_commands = CommandGroup()
    _return_commands = CommandGroup()

    def __init__(self, robot, configfile="/home/lvuser/configs/auto.ini"):
        super().__init__()
        self._robot = robot
        self._config = configparser.ConfigParser()
        self._config.read(configfile)
        self._init_commands()

    def set_match_configuration(self, starting_obs, target_obs, return_obs):
        self._starting_obstacle = starting_obs
        self._target_obstacle = target_obs
        self._return_obstacle = return_obs
        self._obstacle_offset = abs(self._target_obstacle - self._starting_obstacle)
        if (self._target_obstacle > self._starting_obstacle):
            self._obstacle_direction = 1
        elif (self._target_obstacle < self._starting_obstacle):
            self._obstacle_direction = -1
        elif (self._target_obstacle == self._starting_obstacle):
            self._obstacle_direction = 0
        self.add_approach_commands()
        self.add_cross_commands()
        #self.add_score_commands()
        #self.add_return_commands()

    def add_approach_commands(self):
        # lower arm
        self._approach_commands.addParallel(lower_arm_to_count.LowerArm(self._robot, self._lower_bound, self._lower_speed), self._default_timeout)
        # extend hook
        #self._approach_commands.addParallel(extend_hook_to_count.ExtendHookToCount(self._robot, self._extend_speed, self._raise_stop_count))

        if (self._obstacle_offset != 0):
            # turn toward target obstacle
            right_angle = 90 * self._obstacle_direction
            self._approach_commands.addSequential(turn_degrees.TurnDegrees(self._robot, right_angle, self._auto_speed, self._drivetrain_threshold), self._default_timeout)
            # drive toward target obstacle
            alignment_drive = self._obstacle_offset * self._lane_width
            self._approach_commands.addSequential(drive_encoder_counts.DriveEncoderCounts(self._robot, alignment_drive, self._auto_speed, self._drivetrain_threshold), self._default_timeout)
            # turn to face obstacle
            right_angle = right_angle * -1
            self._approach_commands.addSequential(turn_degrees.TurnDegrees(self._robot, right_angle, self._auto_speed, self._drivetrain_threshold), self._default_timeout)

        # drive to obstacle line
        self._approach_commands.addSequential(drive_encoder_counts.DriveEncoderCounts(self._robot, self._distance_to_obstacle, self._auto_speed, self._drivetrain_threshold), self._default_timeout)
        # TODO: MAGIC NUMBER!!! OMG!1!1!!
        #self._approach_commands.addSequential(drive_encoder_counts.DriveEncoderCounts(self._robot, -800, self._auto_speed, self._drivetrain_threshold), self._default_timeout)

        self.addSequential(self._approach_commands)

    def add_cross_commands(self):
        # todo: use pitch gyro to determine if we've crossed, drive until true
        # cross the obstacle
        self._cross_commands.addSequential(drive_encoder_counts.DriveEncoderCounts(self._robot, self._cross_obstacle, self._auto_speed, self._drivetrain_threshold), self._default_timeout)
        # re-center
        self._cross_commands.addSequential(turn_degrees_absolute.TurnDegreesAbsolute(self._robot, 0, self._speed, self._drivetrain_threshold), self._default_timeout)
        self.addSequential(self._cross_commands)

    def add_score_commands(self):
        # angle of hyp/adj
        angle = math.degrees(math.atan(self._target_point / self._lane_width))
        # length of hyp
        hypotenuse = math.sqrt((self._target_point ** 2) + (self._lane_width ** 2))

        if (self._target_obstacle == 1 or self._target_obstacle == 4):
            # turn to the right at [angle]
            self._score_commands.addSequential(turn_degrees.TurnDegrees(self._robot, angle, self._auto_speed, self._drivetrain_threshold), self._default_timeout)
            # drive to the target point along hyp
            self._score_commands.addSequential(drive_encoder_counts.DriveEncoderCounts(self._robot, hypotenuse, self._auto_speed, self._drivetrain_threshold), self._default_timeout)
            # assuming 45 is the angle of the goal relative to the back wall?
            if (self._target_obstacle == 1):
                # turned [angle] toward goal, turn remainder of 45
                self._score_commands.addSequential(turn_degrees.TurnDegrees(self._robot, (45 - angle), self._auto_speed, self._drivetrain_threshold), self._default_timeout)
            elif (self._target_obstacle == 4):
                # turned away from goal by [angle], undo that turn then turn another -45 to face goal
                self._score_commands.addSequential(turn_degrees.TurnDegrees(self._robot, ((angle * -1) - 45), self._auto_speed, self._drivetrain_threshold), self._default_timeout)
        elif (self._target_obstacle == 2 or self._target_obstacle == 5):
            # drive to the target point along adj
            self._score_commands.addSequential(drive_encoder_counts.DriveEncoderCounts(self._robot, self._target_point, self._auto_speed, self._drivetrain_threshold), self._default_timeout)
            if (self._target_obstacle == 2):
                # turn to face goal
                self._score_commands.addSequential(turn_degrees.TurnDegrees(self._robot, 45, self._auto_speed, self._drivetrain_threshold), self._default_timeout)
            elif (self._target_obstacle == 5):
                # turn to face goal
                self._score_commands.addSequential(turn_degrees.TurnDegrees(self._robot, -45, self._auto_speed, self._drivetrain_threshold), self._default_timeout)
        elif (self._target_obstacle == 3):
            # turn to -[angle]
            self._score_commands.addSequential(turn_degrees.TurnDegrees(self._robot, (angle * -1), self._auto_speed, self._drivetrain_threshold), self._default_timeout)
            # drive to the target point along hyp
            self._score_commands.addSequential(drive_encoder_counts.DriveEncoderCounts(self._robot, hypotenuse, self._auto_speed, self._drivetrain_threshold), self._default_timeout)
            # turn to face goal
            self._score_commands.addSequential(turn_degrees.TurnDegrees(self._robot, (angle + 45), self._auto_speed, self._drivetrain_threshold), self._default_timeout)
        # drive toward goal
        self._score_commands.addSequential(drive_encoder_counts.DriveEncoderCounts(self._robot, self._shoot_point, self._auto_speed, self._drivetrain_threshold), self._default_timeout)
        # shoot
        self._score_commands.addSequential(feed_ball_out.FeedBallOut(self._robot, self._feeder_speed, self._feed_time), self._default_timeout)
        self.addSequential(self._score_commands)

    def add_return_commands(self):
        # todo: drive to return obstacle
        # turn around
        # self._return_commands.addSequential(turn_degrees.TurnDegrees(self._robot, 180, self._auto_speed, self._drivetrain_threshold))
        # return to target point
        # self._return_commands.addSequential(drive_encoder_counts.DriveEncoderCounts(self._robot, self._shoot_point, self._auto_speed, self._drivetrain_threshold))
        #

        if (self._target_obstacle == 1 or self._target_obstacle == 2 or self._target_obstacle == 3):
            # turn to face obstacles
            self._return_commands.addSequential(turn_degrees.TurnDegrees(self._robot, 135, self._auto_speed, self._drivetrain_threshold), self._default_timeout)
        elif (self._target_obstacle == 4 or self._target_obstacle == 5):
            # turn to face obstaclces
            self._return_commands.addSequential(turn_degrees.TurnDegrees(self._robot, -135, self._auto_speed, self._drivetrain_threshold), self._default_timeout)
        # drive to obstacles
        self._return_commands.addSexquential(drive_encoder_counts.DriveEncoderCounts(self._robot, self._target_point, self._auto_speed, self._drivetrain_threshold), self._default_timeout)
        self.addSequential(self._return_commands)

    def _init_commands(self):
        # drivetrain
        self._distance_to_obstacle = self._config.getint(self._drivetrain_section, "DISTANCE_TO_OBSTACLE")
        self._auto_speed = self._config.getfloat(self._drivetrain_section, "AUTO_SPEED")
        self._drivetrain_threshold = self._config.getint(self._drivetrain_section, "THRESHOLD")
        self._cross_obstacle = self._config.getint(self._drivetrain_section, "CROSS_OBSTACLE")
        self._target_point = self._config.getint(self._drivetrain_section, "TARGET_POINT")
        self._lane_width = self._config.getint(self._drivetrain_section, "LANE_WIDTH")
        self._shoot_point = self._config.getint(self._drivetrain_section, "SHOOT_POINT")

        # feeder
        self._feeder_speed = self._config.getfloat(self._feeder_section, "FEEDER_SPEED")
        self._feed_time = self._config.getfloat(self._feeder_section, "FEED_TIME")

        # arm
        self._lower_bound = self._config.getint(self._arm_section, "LOWER_BOUND")
        self._lower_speed = self._config.getfloat(self._arm_section, "LOWER_SPEED")

        # hook
        self._extend_speed = self._config.getfloat(self._hook_section, "EXTEND_SPEED")
        self._raise_stop_count = self._config.getint(self._hook_section, "RAISE_STOP_COUNT")

    def end(self):
        """Called once after isFinished returns true"""
        self._robot.drivetrain.arcade_drive(0,0)
        self._robot.feeder.spinFeeder(0)
        self._robot.hook.move_hook(0)
        self._robot.arm.move_arm(0)

    def interrupted(self):
        """Called when another command which requires one or more of the same subsystems is scheduled to run"""
        self.end()
