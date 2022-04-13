from peripherals.motor import Motor

class Drive:
    def __init__(self, l_motor:Motor, r_motor:Motor):
        self.l_motor = l_motor
        self.r_motor = r_motor
    
    def driveForward(self):
        self.l_motor.driveForward()
        self.r_motor.driveForward()
        print("Driving Forward")

    def driveBackward(self):
        self.l_motor.driveBackward()
        self.r_motor.driveBackward()
        print("Driving Backward")

    def turnLeft(self):
        self.l_motor.driveBackward()
        self.r_motor.driveForward()
        print("Turning Left")

    def turnRight(self):
        self.l_motor.driveForward()
        self.r_motor.driveBackward()
        print("Turning Right")
    
    def stop(self):
        self.l_motor.stop()
        self.r_motor.stop()
        print("Stopping")
    