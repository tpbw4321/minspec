import RPi.GPIO as GPIO
from EventManager.Event import EventQueue
from StateMachine.MainHSM import MainHSMProcess
from sensing.button import ButtonService
from threading import Thread
import time


eq = EventQueue(MainHSMProcess)

L_BUMPER = 38
R_BUMPER = 40

buttons = [
    L_BUMPER,
    R_BUMPER
]

bs = ButtonService(buttons)

threads = [
    Thread(target=eq.Process),
    Thread(target=bs.Process, args=(eq, ))
]

def StartServiceThreads(threads:list):
    for thread in threads:
        thread.start()
    while True:
        time.sleep(500)

if __name__ == "__main__":
    try:
        StartServiceThreads(threads)
        # eq.EventQueueProcess()
    except:
        GPIO.cleanup()
        