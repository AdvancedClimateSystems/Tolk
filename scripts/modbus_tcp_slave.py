#!/usr/bin/env python
""" Modbus slave listening at a port.

Usage:
    modbus_tcp_slave.py [--host=<name> --port=<nr>]

Options:
    -h --help       Show this screen.
    --host=<name>   Name of host [default: ""].
    --port=<nr>     The port where slave is listening at [default: 502].

"""
import sys
import time
from docopt import docopt

from logbook import Logger, StreamHandler
from modbus_tk.utils import create_logger
import modbus_tk.defines as cst
from modbus_tk.modbus_tcp import TcpServer

StreamHandler(sys.stdout).push_application()
log = Logger(__name__)

logger = create_logger(name="console", record_format="%(message)s")


def main():
    args = docopt(__doc__)
    server = TcpServer(port=int(args['--port']))
    slave = server.add_slave(1)

    slave.add_block(0, cst.ANALOG_INPUTS, 0, 100)
    log.info('Add analog inputs data block from register 0 to 99 on slave 1')
    slave.add_block(1, cst.DISCRETE_INPUTS, 0, 100)
    log.info('Add discrete inputs data block from register 0 to 99 on slave 1')
    slave.add_block(2, cst.COILS, 100, 100)
    log.info('Add coils data block from register 100 to 199 on slave 1')
    slave.add_block(3, cst.HOLDING_REGISTERS, 100, 100)
    log.info('Add holding registers block from register 100 to 199 on slave 1')

    server.start()
    log.info('TcpServer started listening at port {0}.'.format(args['--port']))

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        log.info('Received SIGINT. Exiting')
    finally:
        server.stop()
        log.info('TcpServer has stopped.')


if __name__ == "__main__":
    main()
