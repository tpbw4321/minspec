from signal import signal
import RPi.GPIO as GPIO
from enum import Enum
from sensing.button import ButtonEvent, L_BUMPER, R_BUMPER
from EventManager.Event import Event
from peripherals.motor import Motor
from peripherals.drive import Drive
import signal
import time

class MainHSMState(Enum):
    STOP = 0
    FORWARD = 1
    BACKWARD = 2
    
R_MOTOR_A = 31
R_MOTOR_B = 33
L_MOTOR_A = 35
L_MOTOR_B = 37

GPIO.setmode(GPIO.BOARD)
HSMState = MainHSMState.STOP

l_motor = Motor(L_MOTOR_A, L_MOTOR_B)
r_motor = Motor(R_MOTOR_A, R_MOTOR_B)

drive = Drive(l_motor, r_motor)

def signal_handler(signum, frame):
    drive.stop()
    GPIO.cleanup()
    exit()

signal.signal(signal.SIGINT, signal_handler)

def MainHSMProcess(event:Event):
    global HSMState
    print(f'{HSMState}')
    if HSMState == MainHSMState.STOP:
        if event.eventType == ButtonEvent.DOWN:
            drive.driveForward()
            HSMState = MainHSMState.FORWARD
    elif HSMState == MainHSMState.FORWARD:
        if event.eventType == ButtonEvent.DOWN:
            drive.driveBackward()
            HSMState = MainHSMState.BACKWARD
    elif HSMState == MainHSMState.BACKWARD:
        if event.eventType == ButtonEvent.UP:
            if event.data == R_BUMPER:
                drive.turnLeft()
                time.sleep(1)
                drive.driveForward()
                HSMState = MainHSMState.FORWARD
            elif event.data == L_BUMPER:
                drive.turnRight()
                time.sleep(1)
                drive.driveForward()
                HSMState = MainHSMState.FORWARD
            else:
                drive.stop()
                HSMState = MainHSMState.STOP
    else:
        print(f'{HSMState} not handled')
        

