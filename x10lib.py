#!/usr/bin/python3

import struct

# House code as determined by letter (A-P)
class HouseCode:
    def __init__(self, letter):
        letter = letter.upper()

        # Accept only letters between A and P, inclusive.
        if not ("A" <= letter <= "P"):
            raise ValueError("House code {} invalid \
(A <= code <= P)".format(letter))

        self.letter = letter

    def __str__(self):
        return self.letter

    def __int__(self):
        return ord(self.letter) - ord("A")

    def __repr__(self):
        return "'{}'".format(self.letter)

# Device unit determined by number (1-16).
class Unit:
    def __init__(self, number):
        # Accept only numbers between 1 and 16, inclusive.
        if not (1 <= number <= 16):
            raise ValueError("Unit {} invalid \
(1 <= unit <= 16)".format(number))

        self.number = number - 1

    def __str__(self):
        return "{:02d}".format(self.number + 1)

    def __int__(self):
        return self.number

    def __repr__(self):
        return str(self.number + 1)

ACTIONS = [
         # One-way codes
    "k", # (Kill) All units off
    "L", # All lights on
    "+", # On
    "-", # Off
    "d", # Dim
    "b", # Brighten
    "l", # All lights off
    "e", # Extended code
         # Two-way codes
    "h", # Hail request
    "H", # Hail acknowledge
    "p", # Pre-set dim
    "S", # Status is on
    "s", # Status is off
    "R"  # Request device status 
]

# Turn the unit on, off, brighten, or dim.
class Action:
    def __init__(self, action):
        # Accept only True, False, +, -, B, and D.
        if type(action) == bool:
            if action:
                self.action = "+"
            else:
                self.action = "-"

        else:
            if action in ACTIONS:
                self.action = action
                self.code = ACTIONS.index(action)
            else:
                raise ValueError("Action {} invalid \
(action must be in {})".format(action, ACTIONS))

    def __str__(self):
        return self.action

    def __int__(self):
        return self.code

    def __repr__(self):
        return "'{}'".format(self.action)

# Complete signal to a device, including housecode, unit, and action.
class Signal:
    def __init__(self, housecode, unit, action, repetitions=1):
        # Ensure that the housecode and unit are of the appropriate
        # class types.
        if type(housecode) != HouseCode:
            housecode = HouseCode(housecode)

        if type(unit) != Unit:
            unit = Unit(unit)

        if type(action) != Action:
            action = Action(action)

        self.housecode = housecode
        self.unit = unit
        self.action = action
        self.control = False # Not implemented

        # Store the number of repetitions, if given, but it must be at
        # least 1.
        self.repetitions = max(repetitions, 1)

    def format(self, std):
        if std == "plain":
            args = self.__dict__
            if "repetitions" not in args:
                args["repetitions"] = ""
            return "{housecode}{unit}{action}{repetitions:02d}".format(**args)
        elif std == "json":
            return str(self.__dict__)
        elif std == "fixedwidth":
            return "{housecode}{unit}{action}{repetitions:02d}".format(**self.__dict__)
            
    def serialize(self):
        # Nibbles is a big-endian assembled list containing data to be
        # serialized.
        nibbles = []
	
        control_nibble = (1 << 4) | (int(self.control) << 3)
        nibbles.append(control_nibble)

        if self.control: # Not implemented
            pass

        else:
            # The first data nibble is the housecode, folloewd by the
            # unit and action.
            nibbles.append(int(self.housecode)) 
            nibbles.append(int(self.unit))
            nibbles.append(int(self.action))

            # The next two nibbles are the number of repetitions.
            nibbles.append((int(self.repetitions) & 0b11110000) >> 4)
            nibbles.append(int(self.repetitions) & 0b00001111)

        # Add a checksum byte that is the XOR of the other three bytes.
        nibbles.append(nibbles[0] ^ nibbles[2] ^ nibbles[4])
        nibbles.append(nibbles[1] & nibbles[3] & nibbles[5])

        # Concatenate all of the nibbles into bytes.
        b = []
        for nibble0, nibble1 in zip(nibbles[0::2], nibbles[1::2]):
            b.append(bytes([(nibble0 << 4) | nibble1]))

        return struct.pack("!cccc", *b) 

    def __str__(self):
        return self.format("fixedwidth")

    # Return True for all sorting operations, because signals are
    # orderless.
    def __lt__(self, rhs): return True
    def __gt__(self, rhs): return True
    def __le__(self, rhs): return True
    def __ge__(self, rhs): return True

# Signal.parse attempts to parse a signal of either plain or fixed
# width format.
@classmethod
def parseSignal(cls, signal_str):
    # Parse the basic components of the signal first. It follows the
    # format A01+, where A is the housecode, 01 is the unit number,
    # and + is the action.
    housecode = HouseCode(signal_str[0])
    unit = Unit(int(str(signal_str[1:3])))
    action = Action(signal_str[3])

    # If the length of the string is greater than 4, then it also
    # includes a repetition number. Otherwise, just set it to 1.
    if len(signal_str) > 4:
        repetitions = int(signal_str[4:])
    else:
        repetitions = 1

    return cls(housecode, unit, action, repetitions)

Signal.parse = parseSignal

