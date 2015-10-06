import json
import pytest
import socket
from uuid import uuid4


def get_new_socket(name):
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    sock.connect(name)

    return sock


def get_json_rpc_message(method, params):
    """ Create JSON-RPC message from data en return it. """
    return json.dumps({
        'jsonrpc': '2.0',
        'method': method,
        'params': params,
        'id': uuid4().int
    })


def get_socket(socket_path):
    """ Return socket instance connected to socket path. """
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    sock.connect(socket_path)

    return sock


def read_coils(starting_address, quantity, sock):
    """ Send read_coils over socket. """
    msg = get_json_rpc_message('read_coils',
                               {'starting_address': starting_address,
                                'quantity': quantity})
    return send_request(msg, sock)


def read_holding_registers(starting_address, quantity, sock):
    """ Send read_coils over socket. """
    msg = get_json_rpc_message('read_holding_registers',
                               {'starting_address': starting_address,
                                'quantity': quantity})
    return send_request(msg, sock)


def write_single_coil(address, value, sock):
    """ Send write_single_coil request over socket. """
    msg = get_json_rpc_message('write_single_coil', {'address':  address,
                                                     'value': value})
    return send_request(msg, sock)


def write_multiple_coils(starting_address, values, sock):
    """ Send write_multiple_coils request over socket. """
    msg = get_json_rpc_message('write_multiple_coils',
                               {'starting_address': starting_address,
                                'values': values})

    return send_request(msg, sock)


def send_request(msg, sock):
    """ Send request to socket and close socket when recieved response.
    Return both request and response.
    """
    sock.sendall(msg)
    resp = sock.recv(1024)

    sock.close()
    return msg, resp


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


@pytest.mark.skipif(reason='True')
@pytest.mark.parametrize('method', [
    'read_discrete_inputs',
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


def test_read_and_write_holding_registers(running_server):
    """ Test following Modbus methods:
    * methods read_holding_registers, function code 03
    * write_single_register, function code 06
    * write_multiple_registers, function code 16
    """
    # Use read_coils (function code 01) to read coil 100.
    sock = get_socket(running_server.server_address)
    msg, resp = read_holding_registers(starting_address=100, quantity=1,
                                       sock=sock)
    assert json.loads(resp) == get_expected_response(msg, [0])


def test_read_and_write_coils(running_server):
    """ Test following Modbus methods:
    * methods read_coils, function code 01
    * write_single_coil, function code 05
    * write_multiple_coils, function code 15
    """
    # First, use write_single_coil (function code 05) to write 1 to coil 100.
    sock = get_socket(running_server.server_address)
    msg, resp = write_single_coil(address=100, value=1, sock=sock)
    assert json.loads(resp) == get_expected_response(msg, [100, 65280])

    # Use read_coils (function code 01) to read coil 100.
    sock = get_socket(running_server.server_address)
    msg, resp = read_coils(starting_address=100, quantity=1, sock=sock)
    assert json.loads(resp) == get_expected_response(msg, [1])

    # Now, use write_multiple_coils (function code 15) to write 0 to coil 100
    # and 1 to coil 101.
    sock = get_socket(running_server.server_address)
    msg, resp = write_multiple_coils(starting_address=100, values=[0, 1],
                                     sock=sock)
    assert json.loads(resp) == get_expected_response(msg, [100, 2])

    # Read coils 100 and 101 again to verify previous write requsts was
    # succesful.
    sock = get_socket(running_server.server_address)
    msg, resp = read_coils(starting_address=100, quantity=2, sock=sock)
    assert json.loads(resp) == get_expected_response(msg, [0, 1])
