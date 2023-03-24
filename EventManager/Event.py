from enum import Enum
from datetime import datetime

class Event:
    def __init__(self, eventType, data=None):
        self.eventType = eventType
        self.data = data

class EventQueue:
    def __init__(self, eventProcessor=None):
        if not eventProcessor:
            print("eventProcessor is None")
        self.eventQueue = []
        self.eventlist = []
        self.services = []
        self.eventProcessor = eventProcessor

    def EventQueuePush(self, event):
        self.eventQueue.append(event)
    
    def EventQueuePop(self):
        if len(self.eventQueue) > 0:
            return self.eventQueue.pop()
        return None

    def Process(self):
        while True:
            if len(self.eventQueue):
                event = self.eventQueue.pop()
                print(f'{datetime.now()}: {event.eventType}')
                if self.eventProcessor:
                    self.eventProcessor(event)

    def EventQueueRegister(self, services):
        for service in services:
            if hasattr(service,'events'):
                for event in service.events:
                    self.eventlist.append(event)
                self.services.append(service)

def EventQueueTest():
    class EVENTS(Enum):
        EVENT_A = 0
        EVENT_B = 1

    eq = EventQueue()
    eq.EventQueueRegister(EVENTS)
    print(eq.eventlist)

if __name__ == "__main__":
    EventQueueTest()