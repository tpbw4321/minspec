from enum import Enum
from EventManager.Event import Event
from EventManager.Event import EventQueue
import RPi.GPIO as GPIO

class ButtonEvent(Enum):
    UP = 0
    DOWN = 1

class Button:
    def __init__(self, pin=None, eq:EventQueue=None):
        if not pin:
            print("No pin specified")
        
        if not eq:
            print("No event queue specified")

        self.eq = eq
        self.count = 0
        self.pin = pin
        self.buttonHistory = 0xFF

        GPIO.setup(self.pin, GPIO.IN)
        GPIO.add_event_detect(self.pin, GPIO.BOTH, callback=self.ButtonSendEvent, bouncetime=10)

    def ButtonSendEvent(self, channel):
        if GPIO.input(channel):
            self.eq.eventQueue.append(Event(ButtonEvent.UP, self.pin))
        else:
            self.eq.eventQueue.append(Event(ButtonEvent.DOWN, self.pin))

class ButtonService:
    def __init__(self, buttons:list, eq:EventQueue):
        self.eq = eq
        self.buttons = []
        for button in buttons:
            self.buttons.append(Button(button, eq))

if __name__ == '__main__':
    L_BUMPER = 38
    R_BUMPER = 40
    
    GPIO.setmode(GPIO.BOARD)

    buttons = [
        Button(L_BUMPER),
        Button(R_BUMPER)
    ]

    while True:
        for button in buttons:
            event = button.ButtonCheck()
            if event:
                print(f'{event[0]}: {event[1]}')
