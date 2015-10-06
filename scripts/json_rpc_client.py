#!/usr/bin/env python
""" Send JSON-RPC requests.

Usage:
    json_rpc_client read_coils <starting-address> <quantity> [--port=<nr> --slave-id=<nr> --socket=<path>]
    json_rpc_client read_discrete_inputs <starting-address> <quantity> [--port=<nr> --slave-id=<nr> --socket=<path>]
    json_rpc_client read_holding_registers <starting-address> <quantity> [--port=<nr> --slave-id=<nr> --socket=<path>]
    json_rpc_client read_input_registers <starting-address> <quantity> [--port=<nr> --slave-id=<nr> --socket=<path>]
    json_rpc_client write_single_coil <address> <value> [--port=<nr> --slave-id=<nr> --socket=<path>]
    json_rpc_client write_multiple_coils <starting_address> <values> [--port=<nr> --slave-id=<nr> --socket=<path>]

Options:
    -h --help                   Show this screen.
    -p --port=<nr>              Number of serial port [default: 1].
    -s --slave-id=<nr>          Id of slave [default: 1].
    --socket=</tmp/tolk.sock>   Location of Tolk's socket [default: /tmp/tolk.sock].

"""
import json
import socket
from uuid import uuid4
from docopt import docopt

READ = 0
SINGLE_WRITE = 1
MULTIPLE_WRITE = 2


def create_message(method, params):
    """ Return a JSON-RPC formatted string. """
    return json.dumps({
        'jsonrpc': '2.0',
        'method': method,
        'params': params,
        'id': uuid4().int,
    })

if __name__ == '__main__':
    args = docopt(__doc__)

    s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    s.connect('/tmp/tolk.sock')

    method_type = None

    if args['read_coils']:
        method = 'read_coils'
        method_type = READ
    elif args['read_discrete_inputs']:
        method = 'read_discrete_inputs'
        method_type = READ
    elif args['read_holding_registers']:
        method = 'read_holding_registers'
        method_type = READ
    elif args['read_input_registers']:
        method = 'read_input_registers'
        method_type = READ

    elif args['write_single_coil']:
        method = 'write_single_coil'
        method_type = SINGLE_WRITE
    elif args['write_multiple_coils']:
        method = 'write_multiple_coils'
        method_type = MULTIPLE_WRITE

    if method_type == READ:
        params = {
            'starting_address': int(args['<starting-address>']),
            'quantity': int(args['<quantity>']),
            'port': int(args['--port']),
            'slave_id': int(args['--slave-id']),
        }
    elif method_type == SINGLE_WRITE:
        params = {
            'address': int(args['<address>']),
            'value': int(args['<value>']),
            'port': int(args['--port']),
            'slave_id': int(args['--slave-id']),
        }
    elif method_type == MULTIPLE_WRITE:
        # Transform a string like '1,0,13' into a list of integers.
        values = [int(v) for v in args['<values>'].split(',')]

        params = {
            'starting_address': int(args['<starting_address>']),
            'values': values,
            'port': int(args['--port']),
            'slave_id': int(args['--slave-id']),
        }

    msg = create_message(method, params)
    s.sendall(msg)

    resp = json.loads(s.recv(1024))
    s.close()

    print(json.dumps(resp, sort_keys=True, indent=4, separators=(',', ': ')))
