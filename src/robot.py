from wpilib import command
import wpilib

from commands.do_nothing import DoNothing
from oi import OI
from subsystems.arm import Arm
from subsystems.drivetrain import Drivetrain
from subsystems.feeder import Feeder
from subsystems.hook import Hook
from commands.auto_mode import AutoCommandGroup


class MyRobot(wpilib.IterativeRobot):
    oi = None
    drivetrain = None
    feeder = None
    arm = None
    hook = None

    def autonomousInit(self):
        #Schedule the autonomous command
        start_obs = self.oi.get_obstacles("Starting_Obstacle")
        target_obs = self.oi.get_obstacles("Target_Obstacle")
        return_obs = self.oi.get_obstacles("Return_Obstacle")
        self.autonomous_command.set_match_configuration(start_obs, target_obs, return_obs)
        self.autonomous_command.start()

    def testInit(self):
        pass

    # Subsystems

    def teleopInit(self):
        self.teleopInitialized = True

    def disabledInit(self):
        self.disabledInitialized = True

    def robotInit(self):
        """
        This function is called upon program startup and
        should be used for any initialization code.
        """
        self.oi = OI(self)
        self.drivetrain = Drivetrain(self)
        self.feeder = Feeder(self)
        self.arm = Arm(self)
        self.hook = Hook(self)
        
        self.oi.setup_button_bindings()

        self.autonomous_command = AutoCommandGroup(self)
        #Create the command used for the autonomous period
        #self.autonomous_command = ExampleCommand(self)\

    def autonomousPeriodic(self):
        """This function is called periodically during autonomous."""
        command.Scheduler.getInstance().run()

    def teleopPeriodic(self):
        """This function is called periodically during operator control."""
        command.Scheduler.getInstance().run()

    def testPeriodic(self):
        """This function is called periodically during test mode."""
        wpilib.LiveWindow.run()

if __name__ == "__main__":
    wpilib.run(MyRobot)
