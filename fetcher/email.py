import threading
from accounts.notifier import Notifier


class Email(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self) -> None:
        Notifier().notify()

