# import the robot api stuff
import wpilib

# import the custom classes that were made to ease the declaration of the buttons and joysticks
from frc_enums import XboxAxis, XboxButtons, init_buttons

# import all da math
import math

# subclass the IterativeRobot class
class MyRobot(wpilib.IterativeRobot):
    # function that runs when we start up the robot
    def robotInit(self):
        self.contr = wpilib.Joystick(0)                   # initialize the joystick
        init_buttons(self.contr)                          # initialize the XboxButtons class
        self.drive = wpilib.RobotDrive(1, 2, 3, 4)        # set up the robot drive -- 1,2,3,4 are the PWM cable outputs on the RIO
        self.sol = wpilib.Solenoid(0)                     # initialize the solenoid -- 0 is the DIO port
        self.sol.set(False)                               #  set the initial value for the solenoid
        self.armMotor = wpilib.Talon(0)                   # initialize a single motor
        self.enc = wpilib.Encoder(aChannel=3, bChannel=4) # initialze the encoder -- 3,4 are DIO ports
        self.enc.reset()                                  #  makes sure the encoder values start at 0
        self.speed_contr = 1/3                            # speed controller constant
        self.armLocation = 0                              # sets the current arm location
        self.armLocations = [0, 2500, 5000, 7500]         # the different arm location encoder values
        self.manual_arm = True                            # boolean that determines if the arm is under manual control on startup
        self.armspeed = 0                                 # sets arm speed to zero originally

    # this function gets called every 250milliseconds when we
    #  have teleop enabled
    def teleopPeriodic(self):
        self.y = self.contr.getRawAxis(XboxAxis.R_Y)   # gets the y value from the right stick on the controller
        self.x = self.contr.getRawAxis(XboxAxis.R_X)   # gets the x value from the right stick on the controller
        self.rot = self.contr.getRawAxis(XboxAxis.L_X) # gets the x value from the left stick on the controller

        # these if statements allow for a dead area in the controller
        #  that way the robot won't move by itself when the sticks aren't being touched
        if self.x < 0.25 and self.x > -0.25:
            self.x = 0
        if self.rot < 0.25 and self.rot > -0.25:
            self.rot = 0
        if self.y < 0.25 and self.y > -0.25:
            self.y = 0

        # passes all of the x, y, and rotation values into a function that sets the motor's speed
        self.drive.mecanumDrive_Cartesian(self.y * self.speed_contr,
                                          -self.rot * self.speed_contr,
                                          self.x * self.speed_contr,
                                          0)

        # if A is pressed set the solenoid out
        if XboxButtons.A.poll():
            self.sol.set(True)
        # but if it isn't pressed and the solenoid is out, pull it back in
        elif not (XboxButtons.A.poll() and self.sol.get()):
            self.sol.set(False)

        # if the Y button is pressed change the arm to 'auto' mode
        # WIP
        if XboxButtons.Y.poll():
            self.manual_arm = not self.manual_arm
            wpilib.DriverStation.reportError("mode changed\n", False)

        # THIS IS ONLY APPLICABLE TO AUTO-ARM MODE
        #  the bumpers allow for automatic movement by changing the location that we're referencing out of
        #  armLocations
        if XboxButtons.R_bump.poll():
            self.armLocation += 1
        if XboxButtons.L_bump.poll():
            self.armLocation -= 1

        # checks if we're using manual arm control
        if self.manual_arm:
            # if we are then we get our speed straight from the Xbox controller
            self.armspeed = self.contr.getRawAxis(XboxAxis.Z_U) - self.contr.getRawAxis(XboxAxis.Z_D)
        else:
            # if we aren't then we need to do some checks first
            try:
                # trys to reference the location inside of the locations array
                #  if this works then we do nothing but run the code from the "finally" block
                #  if it raises an error then we modify the location
                self.armLocations[self.armLocation]
            except IndexError:
                # an IndexError was raised, so we set the location according to if the original
                #  location was too high for the list, or too low.
                self.armLocation = (min(len(self.armLocations) - 1, self.armLocation)
                                    if self.armLocation > len(self.armLocations) else
                                    max(0, self.armLocation))
            finally:
                # finally, we get the location that we want the encoder to go to
                #  and we get the encoder to go to that location
                cur_enc = self.enc.get()
                if cur_enc != self.armLocations[self.armLocation] and (
                        not cur_enc < 100):
                    self.armspeed = math.copysign(1, self.armLocations[self.armLocation] - cur_enc) * 0.8
        
        # if the solenoid is out then we need to pretend that we have a box
        #  which means that the arm needs to have a little more OOMPH to stay up
        if self.sol.get() and self.enc.get() > 100 and self.armspeed == 0:#(self.armspeed > -0.05 or self.armspeed < 0.05):
            self.armspeed = 0.18
        # if the solenoid is not out, and the current armspeed is 0 (the arm isn't moving)
        #  then we set the speed so that it doesn't fall while it's up
        elif not self.sol.get() and self.enc.get() > 100 and self.armspeed == 0:#(self.armspeed > -0.05 or self.armspeed < 0.05):
            self.armspeed = 0.08
        
        # set the arm speed
        self.armMotor.set(self.armspeed)

        # debugging print messages
        try:
            self.armLocations[self.armLocation]
        except:
            self.armLocation = (min(len(self.armLocations) - 1, self.armLocation)
                                if self.armLocation > len(self.armLocations) else
                                max(0, self.armLocation))
        finally:
            wpilib.DriverStation.reportError(str(self.armLocation) + " " + str(math.copysign(1, self.armLocations[self.armLocation] - self.enc.get()) * 0.8) + "\n", False)

# if this is the main thread, run the MyRobot class
if __name__ == '__main__':
    wpilib.run(MyRobot)
