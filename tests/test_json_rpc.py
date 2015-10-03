import json
import pytest
from uuid import uuid4


def get_json_rpc_message(method, starting_address, quantity, port=1,
                         slave_id=1):
    """ Create JSON-RPC message from data en return it. """
    return json.dumps({
        'jsonrpc': '2.0',
        'method': method,
        'params': {
            'starting_address': starting_address,
            'quantity': quantity,
            'port': port,
            'slave_id': slave_id,
        },
        'id': uuid4().int
    })


def get_expected_response(request_msg, result):
    """ Return a response based on response message and expected result of
    Modbus master,o
    """
    msg = json.loads(request_msg)

    return {
        'jsonrpc': '2.0',
        'result': result,
        'id': msg['id'],
    }


@pytest.mark.parametrize('method', [
    'read_coils',
    'read_discrete_inputs',
    'read_holding_registers',
    'read_input_registers',
])
def test_dispatchers_read_methods(sock, method):
    """ Test the methods Dispatcher.read_coils and
    Dispatcher.read_discrete_inputs by sending the proper JSON-RPC messages
    to the socket. At the other end of this socket a server is listening
    which delegates the requests to a Dispatcher instance. See conftest for
    more info.

    This test is more an intergration test rather than a unit test.

    """
    msg = get_json_rpc_message(method, 100, 1)
    sock.sendall(msg)
    resp = sock.recv(1024)

    assert json.loads(resp) == get_expected_response(msg, [0])
