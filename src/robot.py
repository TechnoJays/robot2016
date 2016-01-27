
from wpilib import command
import wpilib

from subsystems.drivetrain import Drivetrain

class MyRobot(wpilib.IterativeRobot):
    # Subsystems
    drivetrain = Drivetrain(self)
    
    _oi = None

    def robotInit(self):
        """
        This function is called upon program startup and
        should be used for any initialization code.
        """
        self._oi = None
        #Create the command used for the autonomous period
        #self.autonomous_command = ExampleCommand(self)

    def autonomousInit(self):
        #Schedule the autonomous command
        self.autonomous_command.start()

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
