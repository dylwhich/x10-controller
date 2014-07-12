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
    OPCODE_READY_STATUS = 0
    OPCODE_TERMINATE = 1
    OPCODE_ACKNOWLEDGE = 2

    DATA_READY_STATUS_NOT_READY = 0
    DATA_READY_STATUS_READY = 1

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
    COMMAND_ON = 2
    COMMAND_OFF = 3
    COMMAND_ALL_LIGHTS_ON = 1
    COMMAND_ALL_LIGHTS_OFF = 6
    COMMAND_ALL_UNITS_OFF = 0
    COMMAND_BRIGHT = 5
    COMMAND_DIM = 4
    COMMAND_EXTENDED_CODE = 7
    COMMAND_HAIL_REQUEST = 8
    COMMAND_HAIL_ACKNOWLEDGE = 9
    COMMAND_PRE_SET_DIM = 10
    # ??????
    COMMAND_EXTENDED_DATA = 12
    COMMAND_STATUS_ON = 13
    COMMAND_STATUS_OFF = 14
    COMMAND_STATUS_REQUEST = 15

    DESCRIPTIONS = {
        COMMAND_ON: "ON",
        COMMAND_OFF: "OFF",
        COMMAND_ALL_LIGHTS_ON: "LIGHTS ON",
        COMMAND_ALL_LIGHTS_OFF: "LIGHTS OFF",
        COMMAND_ALL_UNITS_OFF: "ALL OFF",
        COMMAND_BRIGHT: "BRIGHT",
        COMMAND_DIM: "DIM",
        COMMAND_EXTENDED_CODE: "EXC",
        COMMAND_HAIL_REQUEST: "HAIL REQ",
        COMMAND_HAIL_ACKNOWLEDGE: "HAIL ACK",
        COMMAND_EXTENDED_DATA: "EXTD",
        COMMAND_STATUS_ON: "S ON",
        COMMAND_STATUS_OFF: "S OFF",
        COMMAND_STATUS_REQUEST: "S REQ"}

    def __init__(self, house='A', unit=1, command=1, repetitions=1, encoded=None):
        if encoded:
            house = chr((encoded[0] & 0x0f) + 65)
            unit = ((encoded[1] & 0xf0) >> 4) + 1
            command = (encoded[1] & 0x0f)
            repetitions = encoded[2] or 1
        self.house = house.upper()
        self.unit = unit
        self.command = command
        self.repetitions = repetitions

    def encode(self):
        # This could definitely be more pythonic. Somehow.
        t0 = 0x80 | ((ord(self.house.upper()) - ord('A')) & 0x0f)
        t1 = (((self.unit - 1) << 4) & 0xf0) | (self.command & 0x0f)
        t2 = self.repetitions
        tmp = [t0, t1, t2, t0 ^ t1 ^ t2]
        return bytes(tmp)
