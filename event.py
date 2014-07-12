class X10Event:
    UNIT_ALL = 0
    def __init__(self, packet):
        self.packet = packet
        if type(packet) is DataPacket:
            self.house = packet.house
            self.unit = packet.unit or UNIT_ALL
            self.command = packet.command
