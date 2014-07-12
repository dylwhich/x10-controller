class Packet:
    PACKET_LENGTH = 4

    def decode(b):
        """Retuns a Packet object for the given string, or None if it isn't valid."""
        if len(b) != Packet.PACKET_LENGTH:
            return None

        if b[0] ^ b[1] ^ b[2] != b[3] or ((b[0] & 0x80) >> 7) != 1:
            return None

        if (b[0] & 0x40) >> 6 == 1:
            return ControlPacket(encoded=b)
        else:
            return DataPacket(encoded=b)

    def encode(self):
        """Returns a string representation of the current object"""
        pass

class ControlPacket(Packet):
    def __init__(self, opcode=0, data=0, encoded=None):
        if encoded:
            opcode = encoded[0] & 0x0f
            data = (encoded[1] << 8) | encoded[2]
        self.opcode = opcode
        self.data = data

    def encode(self):
        tmp = [0xc0 | opcode & 0x0f, (data >> 8) & 0xff, data & 0xff]
        tmp.append(tmp[0] ^ tmp[1] ^ tmp[2])
        return bytes(tmp)

class DataPacket(Packet):
    COMMAND_ON = 0
    COMMAND_OFF = 1
    COMMAND_ALL_LIGHT_ON = 2
    COMMAND_ALL_LIGHTS_OFF = 3
    COMMAND_ALL_UNITS_ON = 4
    COMMAND_ALL_UNITS_OFF = 5
    COMMAND_BRIGHT = 6
    COMMAND_DIM = 7

    def __init__(self, house='A', unit=1, command=1, repetitions=1, encoded=None):
        if encoded:
            house = chr((encoded[0] & 0x0f) + 65)
            unit = ((encoded[1] & 0xf0) >> 4) + 1
            command = (encoded[1] & 0x0f)
            repetitions = encoded[2] or 1
        self.house = house
        self.unit = unit
        self.command = command
        self.repetitions = repetitions

    def encode(self):
        # This could definitely be more pythonic. Somehow.
        t0 = 0x80 | ((ord(self.house) - 65) & 0x0f)
        t1 = (((self.unit - 1) << 4) & 0xf0) | (self.command & 0x0f)
        t2 = self.repetitions
        tmp = [t0, t1, t2, t0 ^ t1 ^ t2]
        return bytes(tmp)
