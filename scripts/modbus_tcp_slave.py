#!/usr/bin/env python
""" Modbus slave listening at a port.

Usage:
    modbus_tcp_slave.py [--host=<name> | --port=<nr>]

Options:
    -h --help       Show this screen.
    --port=<nr>     The port where slave is listening at [default: 502].

"""
import time
from docopt import docopt

from modbus_tk.utils import create_logger
import modbus_tk.defines as cst
from modbus_tk.modbus_tcp import TcpServer

logger = create_logger(name="console", record_format="%(message)s")

if __name__ == "__main__":
    args = docopt(__doc__)
    server = TcpServer(port=int(args['--port']))
    slave = server.add_slave(1)

    slave.add_block(0, cst.ANALOG_INPUTS, 0, 100)
    slave.add_block(1, cst.DISCRETE_INPUTS, 0, 100)
    slave.add_block(2, cst.COILS, 100, 100)
    slave.add_block(3, cst.HOLDING_REGISTERS, 100, 100)

    server.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        pass
    finally:
        server.stop()
