#!/usr/bin/env python
""" Send JSON-RPC requests.

Usage:
    json_rpc_client read_coils <starting-address> <quantity> [--port=<nr> --slave-id=<nr> --socket=<path>]
    json_rpc_client read_discrete_inputs <starting-address> <quantity> [--port=<nr> --slave-id=<nr> --socket=<path>]
    json_rpc_client read_holding_registers <starting-address> <quantity> [--port=<nr> --slave-id=<nr> --socket=<path>]
    json_rpc_client read_input_registers <starting-address> <quantity> [--port=<nr> --slave-id=<nr> --socket=<path>]

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


def create_message(method, starting_address, quantity, port, slave_id):
    """ Return a JSON-RPC formatted string. """
    return json.dumps({
        'jsonrpc': '2.0',
        'method': method,
        'params': {
            'starting_address': starting_address,
            'quantity': quantity,
            'port': port,
            'slave_id': slave_id,
        },
        'id': uuid4().int,
    })

if __name__ == '__main__':
    args = docopt(__doc__)

    s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    s.connect('/tmp/tolk.sock')

    if args['read_coils']:
        method = 'read_coils'
    elif args['read_discrete_inputs']:
        method = 'read_discrete_inputs'
    elif args['read_holding_registers']:
        method = 'read_holding_registers'
    elif args['read_input_registers']:
        method = 'read_input_registers'

    msg = create_message(method, int(args['<starting-address>']),
                         int(args['<quantity>']), int(args['--port']),
                         int(args['--slave-id']))
    s.sendall(msg)

    resp = json.loads(s.recv(1024))
    s.close()

    print(json.dumps(resp, sort_keys=True, indent=4, separators=(',', ': ')))
