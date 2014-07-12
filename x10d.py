#!/usr/bin/env python
from daemon import Daemon, SerialDispatcher
from serial import Serial
from threading import Thread
import sys

def callback(event):
    print("EVENT: {0.house}{0.unit}: {0.command}".format(event))

def main(args):
    serial_port = args[1]
    baud = 9600
    
    s = Serial(serial_port, baud)
    dispatcher = SerialDispatcher(s)
    daemon = Daemon(dispatcher)
    daemon.subscribe(callback)

    daemon_thread = Thread(target=daemon.listen, name="daemon-listener")
    daemon_thread.start()
    daemon_thread.join()
    s.close()

if __name__ == "__main__":
    # TODO: Parse arguments for things
    main(sys.argv)
