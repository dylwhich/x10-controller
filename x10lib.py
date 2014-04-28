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
    def __init__(self, housecode, unit, action):
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

    def __str__(self):
        return "{housecode}{unit}{action}".format(**self.__dict__)
