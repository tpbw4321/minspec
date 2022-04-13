import RPi.GPIO as GPIO
import sys
import time

A = 38
B = 40
sleepTime = 1

class Motor:
    def __init__(self, a=None, b=None):
        if (not a or not b):
            print("Set pin a and pin b\n")
            return None
        self.a = a
        self.b = b

        GPIO.setup(self.a, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.b, GPIO.OUT, initial=GPIO.LOW)

    def driveForward(self):
        GPIO.output(self.a, GPIO.LOW)
        GPIO.output(self.b, GPIO.HIGH)
    
    def stop(self):
        GPIO.output(self.a, GPIO.LOW)
        GPIO.output(self.b, GPIO.LOW)
    
    def driveBackward(self):
        GPIO.output(self.b, GPIO.LOW)
        GPIO.output(self.a, GPIO.HIGH)


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
