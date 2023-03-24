from signal import signal
import RPi.GPIO as GPIO
from enum import Enum
from sensing.button import ButtonEvent, L_BUMPER, R_BUMPER
from timer import Timer, TimerEvent, TimerAdd, TimerRemove
from EventManager.Event import Event
from peripherals.motor import Motor
from peripherals.drive import Drive
import signal

timer_set = False

class MainHSMState(Enum):
    STOP = 0
    FORWARD = 1
    BACKWARD = 2
    LEFT = 3
    RIGHT = 4
    
R_MOTOR_A = 31
R_MOTOR_B = 33
L_MOTOR_A = 35
L_MOTOR_B = 37

GPIO.setmode(GPIO.BOARD)
HSMState = MainHSMState.STOP

l_motor = Motor(L_MOTOR_A, L_MOTOR_B)
r_motor = Motor(R_MOTOR_A, R_MOTOR_B)

drive = Drive(l_motor, r_motor)

TIMER_ONE_SECOND = None

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

    elif HSMState == MainHSMState.LEFT:
        if event.eventType == TimerEvent.EXPIRED:
            drive.driveForward()
            HSMState = MainHSMState.FORWARD
        elif event.eventType == ButtonEvent.DOWN:
            drive.driveBackward()
            HSMState = MainHSMState.BACKWARD

    elif HSMState == MainHSMState.RIGHT:
        if event.eventType == TimerEvent.EXPIRED:
            drive.driveForward()
            HSMState = MainHSMState.FORWARD
        elif event.eventType == ButtonEvent.DOWN:
            drive.driveBackward()
            HSMState = MainHSMState.BACKWARD
        

    elif HSMState == MainHSMState.BACKWARD:
        global TIMER_ONE_SECOND
        if event.eventType == ButtonEvent.UP:
            if event.data == R_BUMPER:
                TIMER_ONE_SECOND = Timer(1, Event(TimerEvent.EXPIRED))
                TimerAdd(TIMER_ONE_SECOND)
                HSMState = MainHSMState.LEFT
                drive.turnLeft()
            elif event.data == L_BUMPER:
                TIMER_ONE_SECOND = Timer(1, Event(TimerEvent.EXPIRED))
                TimerAdd(TIMER_ONE_SECOND)
                HSMState = MainHSMState.RIGHT
                drive.turnRight()
            else:
                drive.stop()
                HSMState = MainHSMState.STOP
    else:
        print(f'{HSMState} not handled')
        

