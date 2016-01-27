
from configparser import ConfigParser

import wpilib


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

class UserControllers(object):
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
    
    def __init__(self, robot):
        self.robot = robot
        
        _config = ConfigParser.read("../configs/joysticks.ini")
        
        self._init_joystick_binding(_config)
        
        for i in range(2):
            _controllers = self._init_joystick(_config, i)

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
            dead_zone = self._config.getint(config_section, "DEAD_ZONE")
            if abs(value) < dead_zone:
                value = 0.0
        return value
    
    def _init_joystick(self, config, driver):
        config_section = "JoyConfig" + str(driver)
        stick = wpilib.Joystick(config.getint(config_section, "PORT"),
                                config.getint(config_section, "AXES"),
                                config.getint(config_section, "BUTTONS"))
        return stick
        
    def _init_joystick_binding(self, config):
        axisBindingSection = "AxisBindings"
        JoystickAxis.LEFTX = config.getint(axisBindingSection,"LEFTX")
        JoystickAxis.LEFTY = config.getint(axisBindingSection,"LEFTY")
        JoystickAxis.RIGHTX = config.getint(axisBindingSection,"RIGHTX")
        JoystickAxis.RIGHTY = config.getint(axisBindingSection,"RIGHTY")
        JoystickAxis.DPADX = config.getint(axisBindingSection,"DPADX")
        JoystickAxis.DPADY = config.getint(axisBindingSection,"DPADY")
        
        buttonBindingSection = "ButtonBindings"
        JoystickButtons.X = config.getint(buttonBindingSection, "X")
        JoystickButtons.A = config.getint(buttonBindingSection, "A")
        JoystickButtons.B = config.getint(buttonBindingSection, "B")
        JoystickButtons.Y = config.getint(buttonBindingSection, "Y")
        JoystickButtons.LEFTBUMPER = config.getint(buttonBindingSection, "LEFTBUMPER")
        JoystickButtons.RIGHTBUMPER = config.getint(buttonBindingSection, "RIGHTBUMPER")
        JoystickButtons.LEFTTRIGGER = config.getint(buttonBindingSection, "LEFTTRIGGER")
        JoystickButtons.RIGHTTRIGGER = config.getint(buttonBindingSection, "RIGHTTRIGGER")
        JoystickButtons.BACK = config.getint(buttonBindingSection, "BACK")
        JoystickButtons.START = config.getint(buttonBindingSection, "START")
    