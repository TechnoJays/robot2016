from wpilib import command
import wpilib

from commands.do_nothing import DoNothing
from oi import OI
from subsystems.drivetrain import Drivetrain


class MyRobot(wpilib.IterativeRobot):

    def autonomousInit(self):
        #Schedule the autonomous command
        self.autonomous_command = DoNothing(self)
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
        self._oi = OI(self)
        self.drivetrain = Drivetrain(self)
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
