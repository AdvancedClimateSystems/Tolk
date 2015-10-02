#!/usr/bin/env python
""" Tolk

Usage:
    tolk [--socket=<path> | --modbus-host=<host> | --modbus-port=<nr>]

Options:
    -h --help   Show this screen.
    --socket=<path>     Location of Tolk's socket [default: /tmp/tolk.sock].
    --modbus-host=<ip>  IP of Modbus slave [default: localhost].
    --modbus-port=<nr>  Port of Modbus slave [default: 502]

"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                '../'))

from modbus_tk.modbus_tcp import TcpMaster
from SocketServer import UnixStreamServer
from docopt import docopt

from tolk import Dispatcher, Handler


if __name__ == '__main__':
    args = docopt(__doc__)

    modbus_master = TcpMaster(args['--modbus-host'], args['--modbus-port'])
    dispatcher = Dispatcher(modbus_master)

    server = UnixStreamServer(args['--socket'], Handler)
    server.dispatcher = dispatcher

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        os.unlink(args['--socket'])
