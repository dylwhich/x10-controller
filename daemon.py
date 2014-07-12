from packet import Packet, DataPacket, ControlPacket
from serial import Serial

class Daemon:
    def __init__(self, dispatcher):
        self.dispatcher = dispatcher
        self.observers = []

    def subscribe(self, observer):
        """Subscribes an observer callback of the form f(X10Event)"""
        self.listeners.append(observer)

    def unsubscribe(self, observer):
        """Unsubscribes an observer from events"""
        self.observers.remove(observer)

    def on(self, house, unit=None):
        """Sends an on command to the specified house and unit, or entire house if unit is None"""
        if unit:
            return self.raw(DataPacket(house, unit, DataPacket.COMMAND_ON))
        else:
            return self.raw(DataPacket(house, 0, DataPacket.COMMAND_ALL_UNITS_ON))

    def off(self, house, unit=None):
        """Sends an off command to the specified house and unit, or entire house if unit is None"""
        if unit:
            return self.raw(DataPacket(house, unit, DataPacket.COMMAND_OFF))
        else:
            return self.raw(DataPacket(house, 0, DataPacket.COMMAND_ALL_UNITS_OFF))

    def dim(self, house, unit, level):
        return self.raw(DataPacket(house, unit, DataPacket.COMMAND_DIM, repetitions=16-level))

    def raw(self, packet):
        """Sends a raw packet. Be careful!"""
        if dispatcher.dispatch(packet):
            for f in observers:
                event = X10Event(packet)
                f(event)
            return True
        return False

class SerialDispatcher:
    def __init__(self, serial):
        self.serial = serial

    def dispatch(self, packet):
        pass
