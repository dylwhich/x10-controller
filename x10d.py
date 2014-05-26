#!/usr/bin/python3

import sys, os, serial, argparse, threading
import queue
import x10lib as x10

class Daemon:
    def __init__(self, fifo="/etc/x10ctl",
                 statedb="/etc/x10state.db",
                 serial="/dev/ttyACM0"):
        self.fifopath = fifo
        self.statedbpath = statedb
        self.serialpath = serial
        self.signals = queue.PriorityQueue()

    def listenfifo(self):
        # Make the fifo if it doesn't exist.
        try:
            os.mkfifo(self.fifopath)
        except IOError:
            pass

        with open(self.fifopath, "rb") as fifo:
            while True:
                signal_str = fifo.read(6)
                s = x10.Signal.parse(signal_str)
                self.enqueue(s)

    # Put a signal on the queue along with a priority as determined by
    # prioritize(signal).
    def enqueue(self, signal):
        priority = self.prioritize(signal)

        self.signals.put((priority, signal))

    def prioritize(self, signal):
        return 1

    # consume items from the queue and place them on the serial port.
    def consume(self):
        # Open the serial connection.
        conn = serial.Serial(port=self.serialpath)

        # Query the serial port for a "ready" signal.
        # TODO: replace with control signal
        conn.write("READY?")

        # Continuously retrieve from the queue and send them to the
        # serial port. Prioritized signals are sent first.
        while True:
            # Wait until the serial port hears a request for more data.
            conn.read()

            # Once ready, get a signal from the connection and
            # serialize it over.            
            conn.write(self.signals.get().serialize())
            self.signals.task_done()
        
    # Daemonize by listening for signals on the fifo and consume them
    # from the priority queue simultaneously.
    def start(self):
        self.listener = threading.Thread()
        self.listener.run = self.listenfifo

        self.consumer = threading.Thread()
        self.consumer.run = self.consume

        self.listener.start()
        self.consumer.start()

    # Wait for daemonized threads to finish.
    def join(self):
        self.listener.join()
        self.consumer.join()

def log(string):
    print(string)

def main(args):
    daemon = Daemon(fifo=args.fifo,
                    statedb=args.statedb,
                    serial=args.serial)
    daemon.start()
    daemon.join()

def parse(argv):
    parser = argparse.ArgumentParser("Queue and manage x10 signals via x10lib")
    parser.add_argument("--fifo", "-f", default="/etc/x10ctl",
                        help="FIFO to read signals from")
    parser.add_argument("--statedb", default="/etc/x10state.db",
                        help="Database to store unit states in")

    parser.add_argument("--serial", default="/dev/ttyACM0",
                        help="Serial port to use")

    return parser.parse_args(argv)

if __name__ == "__main__":
    sys.exit(main(parse(sys.argv[1:])))
