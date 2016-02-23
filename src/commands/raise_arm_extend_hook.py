from wpilib.command.command import CommandGroup, Command
from commands.raise_arm_to_count import RaiseArmToCount
from commands.extend_hook_to_count import ExtendHookToCount

class RaiseArmExtendHook(CommandGroup):

    def __init__(self, robot, arm_raised_count, hook_extended_count, name=None):
        '''
        Constructor
        '''
        super().__init__(name)
        self.addSequential(RaiseArmToCount(robot, 1.0, arm_raised_count))
        self.addSequential(ExtendHookToCount(robot, 1.0, hook_extended_count))
