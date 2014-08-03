#!/usr/bin/env python
from daemon import Daemon, SerialDispatcher
from serial import Serial
import api
from threading import Thread
import sys

def callback(event):
    if event:
        print(str(event))

def listen(daemon):
    while True:
        house, unit, act = input().split()
        unit = int(unit)

        if act.upper() == "ON":
            daemon.on(house, unit)
        elif act.upper() == "OFF":
            daemon.off(house, unit)

def main(args):
    serial_port = args[1]
    baud = 9600
    s = Serial(serial_port, baud)

    dispatcher = SerialDispatcher(s)
    daemon = Daemon(dispatcher)
    daemon.subscribe(callback)

    daemon_thread = Thread(target=daemon.listen, name="daemon-listener")
    daemon_thread.start()

    api_thread = Thread(target=api.run_api, args=(daemon,), name="web-api", daemon=True)
    api_thread.start()

    user_thread = Thread(target=listen, args=(daemon,), name="user-listener")
    user_thread.start()

    user_thread.join()
    daemon_thread.join()
    api_thread.join()
    s.close()

if __name__ == "__main__":
    # TODO: Parse arguments for things
    main(sys.argv)
