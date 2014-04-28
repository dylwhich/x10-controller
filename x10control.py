#!/usr/bin/python3

import x10lib as x10

import sys, argparse

def main(args):
    s = parseSignal(args.signal)

    if args.verbose >= 2: print("Opening {}".format(args.fifo))
    with open(args.fifo, "wb") as fifo:
        if args.verbose >= 2: print("Opened {}".format(args.fifo))
        output = s.format(args.type)

        if args.verbose: print(output)
        if not args.dry: fifo.write(output)

        if args.verbose >= 2: print("Wrote to {}".format(args.fifo))

def parseSignal(signal_str):
    # Parse the basic components of the signal first. It follows the
    # format A01+, where A is the housecode, 01 is the unit number,
    # and + is the action.
    housecode = x10.HouseCode(signal_str[0])
    unit = x10.Unit(int(str(signal_str[1:3])))
    action = x10.Action(signal_str[3])

    # If the length of the string is greater than 4, then it also
    # includes a repetition number. Otherwise, just set it to 1.
    if len(signal_str) > 4:
        repetitions = int(signal_str[4:])
    else:
        repetitions = 1

    return x10.Signal(housecode, unit, action, repetitions)

def parse(argv):
    parser = argparse.ArgumentParser("Send x10 signals from the command line")
    parser.add_argument("--fifo", "-f", help="socket to send commands to",
                        default="/etc/x10ctl")
    parser.add_argument("--type", "-t", choices=["plain", "json", "fixedwidth"],
                        default="plain", help="way to format output")
    parser.add_argument("--verbose", "-v", action="count",
                        help="log output to fifo")
    parser.add_argument("--dry", action="store_true",
                        help="do not output to fifo")
    parser.add_argument("signal")
    return parser.parse_args(argv)
                                     

if __name__ == "__main__":
    sys.exit(main(parse(sys.argv[1:])))
