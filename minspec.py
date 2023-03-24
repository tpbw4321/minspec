import RPi.GPIO as GPIO
from EventManager.Event import EventQueue
from StateMachine.MainHSM import MainHSMProcess
from sensing.button import ButtonService
from threading import Thread
import time
from timer import TimerService

# Setup bumper pins
L_BUMPER = 38
R_BUMPER = 40

buttons = [
    L_BUMPER,
    R_BUMPER
]
class Args:
    def __init__(self, eq:EventQueue, ts:TimerService):
        self.eventQueue = eq
        self.timerService = ts
# Create threads
eq = EventQueue(MainHSMProcess)
bs = ButtonService(buttons)
ts = TimerService(eq)

args = (eq, ts)

threads = [
    Thread(target=eq.Process),
    Thread(target=bs.Process, args=(eq, )),
    Thread(target=ts.Process)
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
        