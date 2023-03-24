from enum import Enum
from threading import Thread
from EventManager.Event import Event, EventQueue
import time

timers = []

class TimerEvent(Enum):
    EXPIRED = 0


class Timer:
    def __init__(self, timeout = 0, event:Event = None):
        self.start = 0
        self.timeout = timeout
        self.event = event

    def TimerStart(self):
        self.start = time.time()

    def TimerExpired(self):
        now = time.time() 
        if (now - self.start) >= self.timeout:
            return True
        return False

class TimerService:
    def __init__(self, eq:EventQueue = None):
        global timers
        self.eq = eq
        self.timers = timers
    
    def TimerAdd(self, timer:Timer):
        if timer not in self.timers:
            timer.TimerStart()
            self.timers.append(timer)

    def TimerRemove(self, timer:Timer):
        self.timers.remove(timer)
    
    def Process(self):
        while True:
            for timer in self.timers:
                if timer.TimerExpired():
                    self.timers.remove(timer)
                    self.eq.EventQueuePush(timer.event)
                    print(f'Time Elasped: {time.time()-timer.start}')
            time.sleep(0.25)

def TimerRemove(timer:Timer):
    global timers
    timers.remove(timer)
    timer = None
    print(f'removed: {timer}')


def TimerAdd(timer:Timer):
    global timers
    timer.TimerStart()
    timers.append(timer)


if __name__ == '__main__':
    print(time.time())
    ts = TimerService(EventQueue())

    print(f'TimerService adding 3 second timeout')
    three_seconds_timer = Timer(3)
    TimerAdd(three_seconds_timer)
    print(f'TimerService adding 1 second timeout')
    TimerAdd(Timer(1))
    print(f'TimerService adding .250 second timeout')
    TimerAdd(Timer(.250))
    TimerRemove(three_seconds_timer)

    while True:
        ts.Process()

    # ts = TimerService(True, True, True)
    # ts_thrd = Thread(target = ts.TimerServiceProcess)
    # ts_thrd.start()
    # while True:
    #     if len(ts.eventQueue) > 0:
    #         event = ts.eventQueue.pop()
    #         print(f'{event[0]}: {event[1]}')
