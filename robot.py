import wpilib
from frc_enums import XboxAxis, XboxButton


class MyRobot(wpilib.IterativeRobot):
    def robotInit(self):
        self.contr = wpilib.Joystick(0)
        self.drive = wpilib.RobotDrive(1, 2, 3, 4)
        self.sol = wpilib.Solenoid(0)
        self.sol.set(False)
        self.armMotor = wpilib.Talon(0)
        self.enc = wpilib.Encoder(aChannel=3, bChannel=4)
        self.enc.reset()
        self.speed_contr = 1/3

    def teleopPeriodic(self):
        self.y = self.contr.getRawAxis(XboxAxis.R_Y)
        self.x = self.contr.getRawAxis(XboxAxis.R_X)
        self.rot = self.contr.getRawAxis(XboxAxis.L_X)
        
        if self.x < 0.25 and self.x > -0.25:
            self.x = 0
        if self.rot < 0.25 and self.rot > -0.25:
            self.rot = 0
        if self.y < 0.25 and self.y > -0.25:
            self.y = 0
        
        self.armspeed = self.contr.getRawAxis(XboxAxis.Z_U) - self.contr.getRawAxis(XboxAxis.Z_D)
        self.drive.mecanumDrive_Cartesian(self.y * self.speed_contr,
                                          -self.rot * self.speed_contr,
                                          self.x * self.speed_contr,
                                          0)
        
        self.armMotor.set(self.armspeed)
        
        if self.contr.getRawButton(XboxButton.A):
            self.sol.set(True)
        elif not (self.contr.getRawButton(XboxButton.A) and self.sol.get()):
            self.sol.set(False)
        
        if self.contr.getRawButton(XboxButton.R_bump):
            wpilib.DriverStation.reportError("not implemented yet")
        if self.contr.getRawButton(XboxButton.L_bump):
            wpilib.DriverStation.reportError("not implemented yet")
        
        if self.sol.get() and self.enc.get() > 100 and self.armspeed == 0:
            self.armMotor.set(.08)
        elif not self.sol.get() and self.enc.get() > 100 and self.armspeed == 0:
            self.armMotor.set(.18)
        
        # to check on the encoder position
        #wpilib.DriverStation.reportError("encoder pos: " + str(self.enc.get()) + "armspeed: " + str(self.armspeed), False)

if __name__ == '__main__':
    wpilib.run(MyRobot)
