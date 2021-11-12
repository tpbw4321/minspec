#!/usr/bin/env python

# Copyright (c) 2019, NVIDIA CORPORATION. All rights reserved.
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.

import RPi.GPIO as GPIO
import signal
import sys
import time

A = 20
B = 21
sleepTime = 1

class motor:
    def __init__(self, a=None, b=None):
        if (not a or not b):
            print("Set pin a and pin b\n")
            return None
        self.a = a
        self.b = b

        GPIO.setup(self.a, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.b, GPIO.OUT, initial=GPIO.LOW)
        self.stop()

    def driveForward(self):
        print("Driving Forward")
        GPIO.output(self.a, GPIO.LOW)
        GPIO.output(self.b, GPIO.HIGH)
    
    def stop(self):
        print("Stopping")
        GPIO.output(self.a, GPIO.LOW)
        GPIO.output(self.b, GPIO.LOW)
    
    def driveBackward(self):
        print("Driving Backward")
        GPIO.output(self.a, GPIO.HIGH)
        GPIO.output(self.b, GPIO.LOW)


def signal_handler(sig, frame):
    print('You pressed Ctrl+C!')
    GPIO.cleanup()
    sys.exit(0)

def main():
    # Pin Setup:
    GPIO.setmode(GPIO.BCM)  # BCM pin-numbering scheme from Raspberry Pi

    l_motor = motor(A, B)
    # l_motor.driveForward()

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
    main()
