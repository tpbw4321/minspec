import RPi.GPIO as GPIO
from enum import Enum
from sensing.button import ButtonEvent
from peripherals.motor import Motor

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

def MainHSMProcess(event):
    global HSMState
    if HSMState == MainHSMState.STOP:
        if event == ButtonEvent.DOWN:
            HSMState = MainHSMState.FORWARD
            l_motor.driveForward()
            r_motor.driveForward()
    elif HSMState == MainHSMState.FORWARD:
        if event == ButtonEvent.DOWN:
            HSMState = MainHSMState.BACKWARD
            l_motor.driveBackward()
            r_motor.driveBackward()
    elif HSMState == MainHSMState.BACKWARD:
         if event == ButtonEvent.UP:
            HSMState = MainHSMState.STOP
            l_motor.driveForward()
            r_motor.driveForward()
    else:
        print(f'{HSMState} not handled')
        

