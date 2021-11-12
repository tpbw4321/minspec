from EventManager.Event import Event
from EventManager.Event import EventQueue
import RPi.GPIO as GPIO
import time
import random

serviceId = 1
button = 26

class ButtonService:
    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(button, GPIO.IN)
    
    def ButtonServiceProcess(self, queue:EventQueue):
        while True:
            if GPIO.input(button) == 0:
                event = Event(1, eventCB, random.randint(1, 100000))
                queue.EventQueuePush(event)

            time.sleep(0.125)

def eventCB(event:Event):
    print("EventType: %d Data: %d" % (event.eventType, event.data))