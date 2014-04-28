#!/usr/bin/python3

import x10lib as x10

import sys, argparse

def main(args):
    s = x10.Signal.parse(args.signal)

    if args.verbose >= 2: print("Opening {}".format(args.fifo))
    with open(args.fifo, "wb") as fifo:
        if args.verbose >= 2: print("Opened {}".format(args.fifo))
        output = s.format(args.type)

        if args.verbose: print(output)
        if not args.dry: fifo.write(output)

        if args.verbose >= 2: print("Wrote to {}".format(args.fifo))

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
