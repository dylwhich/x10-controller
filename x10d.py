#!/usr/bin/env python
from daemon import Daemon, SerialDispatcher
from serial import Serial

if __name__ == "__main__":
    # TODO: Get these from arguments
    serial_port = "/dev/ttyACM0"
    baud = 9600
    
    s = Serial(serial_port, baud)
    dispatcher = SerialDispatcher(s)
    daemon = Daemon(dispatcher)

    daemon_thread = Thread(target=daemon.listen, name="daemon-listener"))
    daemon_thread.start()
    daemon_thread.join()
