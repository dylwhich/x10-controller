#!/usr/bin/python3

# House code as determined by letter (A-P)
class HouseCode:
    def __init__(self, letter):
        letter = letter.upper()

        # Accept only letters between A and P, inclusive.
        if not ("A" <= letter <= "P"):
            raise OutOfBoundsException("House code {} \
out of bounds (A <= code <= P)".format(letter))

        self.letter = letter

    def __str__(self):
        return self.letter

    def __repr__(self):
        return "'{}'".format(self.letter)

# Device unit determined by number (1-16).
class Unit:
    def __init__(self, number):
        # Accept only numbers between 1 and 16, inclusive.
        if not (1 <= number <= 16):
            raise OutOfBoundsException("Unit {} \
out of bounds (1 <= unit <= 16)".format(number))

        self.number = number

    def __str__(self):
        return "{:02d}".format(self.number)

    def __repr__(self):
        return str(self.number)

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
            action = action.upper()
            if action in [ "+", "-", "B", "D" ]:
                self.action = action
            else:
                raise KeyError("Action {} invalid \
(action must be True, False, +, -, B, or D)".format(action))

    def __str__(self):
        return self.action

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

        # Store the number of repetitions, if given, but it must be at
        # least 1.
        self.repetitions = max(repetitions, 1)

    def format(self, std):
        if std == "plain":
            return str(self)
        elif std == "json":
            return str(self.__dict__)
        elif std == "fixedwidth":
            return "{housecode}{unit}{action}{repetitions:02d}".format(**self.__dict__)
            

    def __str__(self):
        args = self.__dict__
        if self.repetitions > 1:
            args["repetitions"] = ""

        return "{housecode}{unit}{action}{repetitions}".format(**args)

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
