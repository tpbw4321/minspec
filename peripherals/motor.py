from enum import Enum
import RPi.GPIO as GPIO
import sys
import time

A = 38
B = 40
sleepTime = 1

class MotorState(Enum):
    STATE_UNKNOWN = 0
    STATE_STOP = 1
    STATE_FORWARD = 2
    STATE_BACKWARD = 3

class Motor:
    def __init__(self, a=None, b=None):
        if (not a or not b):
            print("Set pin a and pin b\n")
            return None
        self.a = a
        self.b = b
        self.state = MotorState.STATE_UNKNOWN

        GPIO.setup(self.a, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.b, GPIO.OUT, initial=GPIO.LOW)

    def driveForward(self):
        print("Driving Forward")
        GPIO.output(self.a, GPIO.LOW)
        GPIO.output(self.b, GPIO.HIGH)
        self.state = MotorState.STATE_FORWARD
    
    def stop(self):
        print("Stopping")
        GPIO.output(self.a, GPIO.LOW)
        GPIO.output(self.b, GPIO.LOW)
        self.state = MotorState.STATE_STOP
    
    def driveBackward(self):
        print("Driving Backward")
        GPIO.output(self.a, GPIO.HIGH)
        GPIO.output(self.b, GPIO.LOW)
        self.state = MotorState.STATE_BACKWARD


def signal_handler(sig, frame):
    print('You pressed Ctrl+C!')
    GPIO.cleanup()
    sys.exit(0)

def MotorTest():
    # Pin Setup:
    GPIO.setmode(GPIO.BOARD)  # BCM pin-numbering scheme from Raspberry Pi

    l_motor = Motor(A, B)

    print("Starting demo now! Press CTRL+C to exit")

    try:
        while True:
            l_motor.driveForward()
            time.sleep(sleepTime)
            l_motor.driveBackward()
            time.sleep(sleepTime)
            continue
    finally:
        GPIO.cleanup()

if __name__ == '__main__':
    MotorTest()
