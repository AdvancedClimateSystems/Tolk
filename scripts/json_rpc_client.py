#!/usr/bin/env python
""" Send JSON-RPC requests.

Usage:
    json_rpc_client read_coils <starting-address> <quantity> [--slave-id=<nr> --socket=<path>]
    json_rpc_client read_discrete_inputs <starting-address> <quantity> [--slave-id=<nr> --socket=<path>]
    json_rpc_client read_holding_registers <starting-address> <quantity> [--slave-id=<nr> --socket=<path>]
    json_rpc_client read_input_registers <starting-address> <quantity> [--slave-id=<nr> --socket=<path>]
    json_rpc_client write_single_coil <address> <value> [--slave-id=<nr> --socket=<path>]
    json_rpc_client write_single_register <address> <value> [--slave-id=<nr> --socket=<path>]
    json_rpc_client write_multiple_coils <starting_address> <values> [--slave-id=<nr> --socket=<path>]
    json_rpc_client write_multiple_registers <starting_address> <values> [--slave-id=<nr> --socket=<path>]

Options:
    -h --help                   Show this screen.
    -s --slave-id=<nr>          Id of slave [default: 1].
    --socket=</tmp/tolk.sock>   Location of Tolk's socket [default: /tmp/tolk.sock].

"""
import json
import socket
from uuid import uuid4
from docopt import docopt
from collections import namedtuple

READ = 0
SINGLE_WRITE = 1
MULTIPLE_WRITE = 2

Method = namedtuple('Method', ['name', 'type_'])


def main():
    args = docopt(__doc__)

    s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    s.connect('/tmp/tolk.sock')

    if args['read_coils']:
        method = Method(name='read_coils',  type_=READ)
    elif args['read_discrete_inputs']:
        method = Method(name='discrete_inputs',  type_=READ)
    elif args['read_holding_registers']:
        method = Method(name='read_holding_registers', type_=READ)
    elif args['read_input_registers']:
        method = Method(name='read_input_registers', type_=READ)
    elif args['write_single_coil']:
        method = Method(name='write_single_coil', type_=SINGLE_WRITE)
    elif args['write_single_register']:
        method = Method(name='write_single_register', type_=SINGLE_WRITE)
    elif args['write_multiple_coils']:
        method = Method(name='write_multiple_coils', type_=MULTIPLE_WRITE)
    elif args['write_multiple_registers']:
        method = Method(name='write_multiple_registers', type_=MULTIPLE_WRITE)

    if method.type_ == READ:
        params = {
            'starting_address': int(args['<starting-address>']),
            'quantity': int(args['<quantity>']),
        }
    elif method.type_ == SINGLE_WRITE:
        params = {
            'address': int(args['<address>']),
            'value': int(args['<value>']),
        }
    elif method.type_ == MULTIPLE_WRITE:
        # Transform a string like '1,0,13' into a list of integers.
        values = [int(v) for v in args['<values>'].split(',')]

        params = {
            'starting_address': int(args['<starting_address>']),
            'values': values,
        }

    params['slave_id'] = int(args['--slave-id'])

    msg = get_json_rpc_message(method.name, params)
    s.sendall(msg)

    resp = json.loads(s.recv(1024))
    s.close()

    print(json.dumps(resp, sort_keys=True, indent=4, separators=(',', ': ')))


def get_json_rpc_message(method, params):
    """ Return a JSON-RPC formatted string.

    :param method: Name of JSON-RPC method.
    :param params: Dictionary with JSON-RPC parameters.
    :return: JSON-RPC valid string.
    """
    return json.dumps({
        'jsonrpc': '2.0',
        'method': method,
        'params': params,
        'id': uuid4().int,
    })

if __name__ == '__main__':
    main()
