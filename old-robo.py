import wpilib
from frc_enums import *


class MyRobot(wpilib.IterativeRobot):

    def robotInit(self):
        self.contr = wpilib.Joystick(0)
        self.drive = wpilib.RobotDrive(0, 1)
        self.drive_const = .7

    def teleopPeriodic(self):
        self.drive.tankDrive(self.contr.getRawAxis(XboxAxis.L_Y) * self.drive_const,
                             self.contr.getRawAxis(XboxAxis.R_Y) * self.drive_const)
        if self.contr.getRawButton(XboxButtons.A):
            self.drive_const += .1
            if self.drive_const >= 1:
                self.drive_const = .1
            print("You hit A")
#        self.drive.mecanumDrive_Cartesian(self.contr.getRawAxis(XboxAxis.R_Y),
#                                  self.contr.getRawAxis(XboxAxis.L_X),
#                                  0)


if __name__ == '__main__':
    wpilib.run(MyRobot)
