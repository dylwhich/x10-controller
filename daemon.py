from packet import Packet, DataPacket, ControlPacket
from serial import Serial
from event import X10Event

DEBUG = False

class Daemon:
    def __init__(self, dispatcher):
        self.dispatcher = dispatcher
        self.observers = []

    def subscribe(self, observer):
        """Subscribes an observer callback of the form f(X10Event)"""
        self.observers.append(observer)

    def unsubscribe(self, observer):
        """Unsubscribes an observer from events"""
        self.observers.remove(observer)

    def report(self, event):
        for f in self.observers:
            f(event)

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
        if self.dispatcher.dispatch(packet):
            event = X10Event(packet)
            self.report(event)
            return True
        return False

    def listen(self):
        """Blocks for events from the dispatcher, forever."""
        while True:
            event = self.dispatcher.next_event()
            # Don't report CONTROL things?

            if event is not None:
                if event.type == X10Event.TYPE_DATA:
                    self.report(event)
                elif event.type == X10Event.TYPE_CONTROL:
                    print(str(event))

class SerialDispatcher:
    def __init__(self, serial):
        self.serial = serial

    def dispatch(self, packet):
        raw_bytes = packet.encode()
        if DEBUG:
            print(hex(int.from_bytes(raw_bytes,byteorder='big')))
        written = self.serial.write(raw_bytes)
        if DEBUG:
            print("written: ", written)
        return written == Packet.PACKET_LENGTH

    def has_event(self):
        return self.serial.inWaiting() >= Packet.PACKET_LENGTH

    def next_event(self):
        raw_bytes = self.serial.read(Packet.PACKET_LENGTH)
        if DEBUG:
            print(hex(int.from_bytes(raw_bytes,byteorder='big')))
        packet = Packet.decode(raw_bytes)
        if packet is not None:
            return X10Event(packet)
        return None
