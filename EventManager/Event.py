class Event:
    def __init__(self, eventType, cb, data):
        self.eventType = eventType
        self.cb = cb
        self.data = data

class EventQueue:
    def __init__(self):
        self.queue = []

    def EventQueuePush(self, event):
        self.queue.append(event)
    
    def EventQueuePop(self):
        if len(self.queue) > 0:
            return self.queue.pop()
        return None

    def EventQueueProcess(self):
        while True:
            e = self.EventQueuePop()
            if e:
                e.cb(e)

def eventCB(event:Event):
    print("EventType: %d Data: %d" % (event.eventType, event.data))

if __name__ == "__main__":
    e = Event(0, eventCB, 5)
    eq = EventQueue()
    eq.EventQueuePush(e)
    eq.EventQueueProcess()