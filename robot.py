import wpilib
from frc_enums import *


class MyRobot(wpilib.IterativeRobot):

    def robotInit(self):
        self.contr = wpilib.Joystick(0)
        self.drive = wpilib.RobotDrive(0, 1)

    def teleopPeriodic(self):
        self.drive.tankDrive(self.controller.getRawAxis(XboxAxis.L_Y),
                             self.controller.getRawAxis(XboxAxis.R_Y))
        if self.contr.getRawButon(XboxButtons.A):
            print("You hit A")
#        self.drive.mecanumDrive_Cartesian(self.contr.getRawAxis(XboxAxis.R_Y),
#                                  self.contr.getRawAxis(XboxAxis.L_X),
#                                  0)


if __name__ == '__main__':
    wpilib.run(MyRobot)
