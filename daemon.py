from packet import Packet
from serial import Serial

class Daemon():
    def __init__(self):
        self.listeners = []
        self.serial = serial
        self.fifo = fifo

    def subscribe(self, observer):
        """Register an observer of the form f(Packet)"""
        listeners.append(observer)

    def unsubscribe(self, observer):
        """Unsubscribes an observer from this"""
        listeners.remove(observer)
