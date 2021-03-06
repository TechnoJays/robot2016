

import configparser
import os
import wpilib
from wpilib.smartdashboard import SmartDashboard
from wpilib.buttons.button import Button
from wpilib.buttons.joystickbutton import JoystickButton
from commands.pick_up_ball import PickUpBall
from commands.retract_hook_to_count import RetractHookToCount
from commands.raise_arm_extend_hook import RaiseArmExtendHook
from commands.shoot_ball import ShootBall
from wpilib.sendablechooser import SendableChooser

class JoystickAxis(object):
    """Enumerates joystick axis."""
    LEFTX = 0
    LEFTY = 1
    RIGHTX = 2
    RIGHTY = 3
    DPADX = 5
    DPADY = 6

class JoystickButtons(object):
    """Enumerates joystick buttons."""
    X = 1
    A = 2
    B = 3
    Y = 4
    LEFTBUMPER = 5
    RIGHTBUMPER = 6
    LEFTTRIGGER = 7
    RIGHTTRIGGER = 8
    BACK = 9
    START = 10

class UserController(object):
    """Enumerates the controllers."""
    DRIVER = 0
    SCORING = 1

class OI:
    """
    This class is the glue that binds the controls on the physical operator
    interface to the commands and command groups that allow control of the robot.
    """
    _config=None
    _command_config = None
    _controllers = []
    _starting_chooser = None
    _target_chooser = None
    _return_chooser = None
    _auto_program_chooser = None

    def __init__(self, robot, configfile='/home/lvuser/configs/joysticks.ini', command_config='/home/lvuser/configs/commands.ini'):
        self.robot = robot
        self._config = configparser.ConfigParser()
        self._config.read(configfile)
        self._command_config = command_config
        self._init_joystick_binding()

        for i in range(2):
            self._controllers.append(self._init_joystick(i))

        self._create_smartdashboard_buttons()

    def setup_button_bindings(self):
        cmdcfg = configparser.ConfigParser()
        cmdcfg.read(self._command_config)

        arm_max_position = cmdcfg.getint("ArmCommands", "RAISED_BOUND")
        hook_max_position = cmdcfg.getint("HookCommands", "EXTENDED_BOUND")

        scoring_right_trigger = JoystickButton(self._controllers[UserController.SCORING], JoystickButtons.RIGHTTRIGGER)
        scoring_a_button = JoystickButton(self._controllers[UserController.SCORING], JoystickButtons.A)
        scoring_y_button = JoystickButton(self._controllers[UserController.SCORING], JoystickButtons.Y)
        scoring_left_trigger = JoystickButton(self._controllers[UserController.SCORING], JoystickButtons.LEFTTRIGGER)

        scoring_right_trigger.whenPressed(ShootBall(self.robot))
        #scoring_y_button.whenPressed(RaiseArmExtendHook(self.robot, arm_max_position, hook_max_position))
        #scoring_a_button.whenPressed(RetractHookToCount(self.robot, 1.0, 0))
        scoring_left_trigger.whenPressed(PickUpBall(self.robot, 1.0, "PickUpBall", 5.0))

    def get_axis(self, user, axis):
        """Read axis value for specified controller/axis.

        Args:
            user: Controller ID to read from
            axis: Axis ID to read from.

        Return:
            Current position for the specified axis. (Range [-1.0, 1.0])
        """
        controller = self._controllers[user]
        value = 0.0
        if axis == JoystickAxis.DPADX:
            value = controller.getPOV()
            if value == 90:
                value = 1.0
            elif value == 270:
                value = -1.0
            else:
                value = 0.0
        elif axis == JoystickAxis.DPADY:
            value = controller.getPOV()
            if value == 0:
                value = -1.0
            elif value == 180:
                value = 1.0
            else:
                value = 0.0
        else:
            config_section = "JoyConfig" + str(user)
            dead_zone = self._config.getfloat(config_section, "DEAD_ZONE")
            value = controller.getRawAxis(axis)
            if abs(value) < dead_zone:
                value = 0.0

        return value

    def _create_smartdashboard_buttons(self):
        self._auto_program_chooser = SendableChooser()
        self._auto_program_chooser.addDefault("Default", 1)
        self._auto_program_chooser.addObject("Do Nothing", 2)
        SmartDashboard.putData("Autonomous", self._auto_program_chooser)

        self._starting_chooser = SendableChooser()
        self._starting_chooser.addDefault("1", 1)
        self._starting_chooser.addObject("2", 2)
        self._starting_chooser.addObject("3", 3)
        self._starting_chooser.addObject("4", 4)
        self._starting_chooser.addObject("5", 5)
        SmartDashboard.putData("Starting_Obstacle", self._starting_chooser)
        self._target_chooser = SendableChooser()
        self._target_chooser.addDefault("1", 1)
        self._target_chooser.addObject("2", 2)
        self._target_chooser.addObject("3", 3)
        self._target_chooser.addObject("4", 4)
        self._target_chooser.addObject("5", 5)
        SmartDashboard.putData("Target_Obstacle", self._target_chooser)
        self._return_chooser = SendableChooser()
        self._return_chooser.addDefault("1", 1)
        self._return_chooser.addObject("2", 2)
        self._return_chooser.addObject("3", 3)
        self._return_chooser.addObject("4", 4)
        self._return_chooser.addObject("5", 5)
        SmartDashboard.putData("Return_Obstacle", self._return_chooser)
        pass

    def get_auto_choice(self):
        return self._auto_program_chooser.getSelected()

    def get_obstacles(self, obstacle):
        value = 1
        if (obstacle == "Starting_Obstacle"):
            value = self._starting_chooser.getSelected()
        elif (obstacle == "Target_Obstacle"):
            value = self._target_chooser.getSelected()
        elif (obstacle == "Return_Obstacle"):
            value = self._return_chooser.getSelected()

        return value

    def _init_joystick(self, driver):
        config_section = "JoyConfig" + str(driver)
        stick = wpilib.Joystick(self._config.getint(config_section, "PORT"),
                                self._config.getint(config_section, "AXES"),
                                self._config.getint(config_section, "BUTTONS"))
        return stick

    def _init_joystick_binding(self):
        axisBindingSection = "AxisBindings"
        JoystickAxis.LEFTX = self._config.getint(axisBindingSection,"LEFTX")
        JoystickAxis.LEFTY = self._config.getint(axisBindingSection,"LEFTY")
        JoystickAxis.RIGHTX = self._config.getint(axisBindingSection,"RIGHTX")
        JoystickAxis.RIGHTY = self._config.getint(axisBindingSection,"RIGHTY")
        JoystickAxis.DPADX = self._config.getint(axisBindingSection,"DPADX")
        JoystickAxis.DPADY = self._config.getint(axisBindingSection,"DPADY")

        buttonBindingSection = "ButtonBindings"
        JoystickButtons.X = self._config.getint(buttonBindingSection, "X")
        JoystickButtons.A = self._config.getint(buttonBindingSection, "A")
        JoystickButtons.B = self._config.getint(buttonBindingSection, "B")
        JoystickButtons.Y = self._config.getint(buttonBindingSection, "Y")
        JoystickButtons.LEFTBUMPER = self._config.getint(buttonBindingSection, "LEFTBUMPER")
        JoystickButtons.RIGHTBUMPER = self._config.getint(buttonBindingSection, "RIGHTBUMPER")
        JoystickButtons.LEFTTRIGGER = self._config.getint(buttonBindingSection, "LEFTTRIGGER")
        JoystickButtons.RIGHTTRIGGER = self._config.getint(buttonBindingSection, "RIGHTTRIGGER")
        JoystickButtons.BACK = self._config.getint(buttonBindingSection, "BACK")
        JoystickButtons.START = self._config.getint(buttonBindingSection, "START")
