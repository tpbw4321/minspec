from EventManager.Event import EventQueue
from sensing.button import ButtonService
from threading import Thread

eq = EventQueue()
bs = ButtonService()

threads = [
    Thread(target = eq.EventQueueProcess),
    Thread(target = bs.ButtonServiceProcess, args = (eq,)),
]

if __name__ == "__main__":
    for thread in threads:
        thread.start()
