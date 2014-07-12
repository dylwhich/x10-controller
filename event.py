from packet import Packet, DataPacket
class X10Event:
    UNIT_ALL = 0
    TYPE_DATA = "data"
    TYPE_CONTROL = "control"

    def __init__(self, packet):
        self.packet = packet
        if type(packet) is DataPacket:
            self.type = X10Event.TYPE_DATA
            self.house = packet.house
            self.unit = packet.unit or UNIT_ALL
            self.command = packet.command
        elif type(packet) is ControlPacket:
            self.type = X10Event.TYPE_CONTROL

    def __str__(self):
        if self.type is X10Event.TYPE_DATA:
            result = "[D] " + self.house
            if self.unit:
                result += " " + str(self.unit)
            result += " " + DataPacket.DESCRIPTIONS[self.command]
        elif self.type is X10Event.TYPE_CONTROL:
            result = "[C]"
        return result
