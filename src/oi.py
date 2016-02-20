

import configparser
import os
import wpilib
from wpilib.smartdashboard import SmartDashboard
from commands import *

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

    _controllers = []

    def __init__(self, robot, configfile = 'joysticks.ini'):
        self.robot = robot
        self._config = configparser.ConfigParser()
        self._config.read(os.path.join(os.getcwd(), configfile))

        self._init_joystick_binding()

        for i in range(2):
            self._controllers.append(self._init_joystick(i))

        self._create_smartdashboard_buttons()

        #CREATING BUTTONS
        #One type of button is a joystick button which is any button on a joystick.
        #You create one by telling it which joystick it's on and which button
        #number it is.
        #stick = wpilib.Joystick(port)
        #button = buttons.JoystickButton(stick, button_number)

        #There are a few additional built-in buttons you can use. Additionally, by
        #subclassing Button you can create custom triggers and bind those to
        #commands the same as any other Button

        #TRIGGERING COMMANDS WITH BUTTONS
        #Once you have a button, it's trivial to bind it to a button in one of
        #three ways;

        #Start the command when the button is pressed and let it run the command
        #until it is finished as determined by it's isFinished method.
        #button.whenPressed(ExampleCommand())

        #Run the command while the button is being held down and interrupt it
        #once the button is released
        #button.whileHeld(ExampleCommand())

        #Start the command when the button is released and let it run the command
        #until it is finished as determined by it's isFinished method.
        #button.whenReleased(ExampleCommand())

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
        SmartDashboard.putData("DriveEncoderCounts",
            commands.drive_encoder_counts.DriveEncoderCounts(self.robot, 100, 1.0, 10, 30))
        SmartDashboard.putData("DriveTime",
            commands.drive_time.DriveTime(self.robot, 2.0, 1.0, 0.3))
        SmartDashboard.putData("ExtendHookToCount",
            commands.extend_hook_to_count.ExtendHookToCount(self.robot, 1.0, 50))
        SmartDashboard.putData("FeedBallOut",
            commands.feed_ball_out.FeedBallOut(self.robot, 1.0, 1.0))
        SmartDashboard.putData("LowerArmToCount",
            commands.lower_arm_to_count.LowerArm(self.robot, 0, 1.0))
        SmartDashboard.putData("PickUpBall",
            commands.pick_up_ball.PickUpBall(self.robot, 0.5))
        SmartDashboard.putData("RaiseArmToCount",
            commands.raise_arm_to_count.RaiseArmToCount(self.robot, 1.0, 50))
        SmartDashboard.putData("RetractHookToCount",
            commands.retract_hook_to_count.RetractHookToCount(self.robot, 1.0, 0))
        SmartDashboard.putData("TurnDegrees",
            commands.turn_degrees.TurnDegrees(self.robot, 90.0, 0.5, 5.0, 10.0))
        SmartDashboard.putData("TurnTime",
            commands.turn_time.TurnTime(self.robot, 1.0, 0.5, 0.3))

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
