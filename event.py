from packet import Packet, DataPacket, ControlPacket
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
            self.opcode = packet.opcode
            self.data = packet.data

    def __str__(self):
        if self.type is X10Event.TYPE_DATA:
            result = "[D] " + self.house
            if 1 <= self.unit <= 16:
                result += " " + str(self.unit)
            result += " " + DataPacket.DESCRIPTIONS[self.command]
        elif self.type is X10Event.TYPE_CONTROL:
            result = "[C] "
            if self.opcode == ControlPacket.OPCODE_READY_STATUS:
                result += "Ready Status: "
                result += "READY" if self.data == ControlPacket.DATA_READY_STATUS_READY else "NOT READY"
            elif self.opcode == ControlPacket.OPCODE_ACKNOWLEDGE:
                result += "Acknowledged"
                if self.data:
                    result += " (" + hex(self.data) + ")"
        return result
