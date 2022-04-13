from enum import Enum
from EventManager.Event import Event
from EventManager.Event import EventQueue
import RPi.GPIO as GPIO
import signal
L_BUMPER = 38
R_BUMPER = 40

BUTTON_MASK = 0b111
BUTTON_DOWN = 0b100
BUTTON_UP   = 0b011

class ButtonEvent(Enum):
    UP = 0
    DOWN = 1

class Button:
    def __init__(self, pin=None):
        if not pin:
            print("No pin specified")
        self.pin = pin
        self.buttonHistory = 0xFF
        GPIO.setup(self.pin, GPIO.IN)

    def ButtonCheck(self)->tuple:
        self.buttonHistory <<= 1
        self.buttonHistory += GPIO.input(self.pin)
        self.buttonHistory &= BUTTON_MASK
        if self.buttonHistory == BUTTON_DOWN:
            return (ButtonEvent.DOWN, self.pin)
        elif self.buttonHistory == BUTTON_UP:
            return (ButtonEvent.UP, self.pin)
        else:
            return None

def signal_handler(signum, frame):
    GPIO.cleanup()
    exit()

signal.signal(signal.SIGINT, signal_handler)

class ButtonService:
    def __init__(self, buttons:list):
        buttonList = []
        for button in buttons:
            buttonList.append(Button(button))
        self.buttons = buttonList
        self.eventQueue = []
        self.events = ButtonEvent
    
    def Process(self, eq:EventQueue):
        while True:
            for button in self.buttons:
                event = button.ButtonCheck()
                if event:
                    eq.EventQueuePush(Event(event[0], event[1]))

if __name__ == '__main__':
    
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
