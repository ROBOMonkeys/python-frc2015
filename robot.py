import wpilib
from frc_enums import *


class MyRobot(wpilib.IterativeRobot):

    def robotInit(self):
        self.controller = wpilib.Joystick(0)
        self.drive = wpilib.RobotDrive(0, 1)

    def teleopPeriodic(self):
        self.drive.tankDrive(self.controller.getRawAxis(XboxAxis.L_Y.value),
                             self.controller.getRawAxis(XboxAxis.R_X.value))
#        self.drive.mecanumDrive_Cartesian(self.controller.getRawAxis(XboxAxis.R_Y.value),
#                                  self.controller.getRawAxis(XboxAxis.L_X.value),
#                                  0)


if __name__ == '__main__':
    wpilib.run(MyRobot)
