from enum import Enum
from threading import Thread
import time

class TimerEvent(Enum):
    SECOND = 0
    MINUTE = 1
    HOUR = 2

class TimerService:
    def __init__(self, second = False, minute = False, hour = False):
        self.events = TimerEvent
        self.eventQueue = []
        self.count = 0
        self.second = second
        self.minute = minute
        self.hour = hour
    
    def Process(self):
        while True:
            self.count = (self.count + 1) % 14400
            if self.second and (self.count % 4) == 0:
                self.eventQueue.append((TimerEvent.SECOND, 0))
            if self.minute and (self.count % 240) == 0:
                self.eventQueue.append((TimerEvent.MINUTE, 0))
            if self.hour and self.count == 0:
                self.eventQueue.append((TimerEvent.HOUR, 0))
            time.sleep(0.25)

            
if __name__ == '__main__':
    ts = TimerService(True, True, True)
    ts_thrd = Thread(target = ts.TimerServiceProcess)
    ts_thrd.start()
    while True:
        if len(ts.eventQueue) > 0:
            event = ts.eventQueue.pop()
            print(f'{event[0]}: {event[1]}')
