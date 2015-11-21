import json
import socket
from uuid import uuid4


def get_json_rpc_message(method, params):
    """ Create JSON-RPC message from data en return it. """
    return json.dumps({
        'jsonrpc': '2.0',
        'method': method,
        'params': params,
        'id': uuid4().int
    })


def get_expected_response(request_msg, result):
    """ Return a response based on response message and expected result of
    Modbus master.
    """
    msg = json.loads(request_msg)

    return {
        'jsonrpc': '2.0',
        'result': result,
        'id': msg['id'],
    }


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


def read_discrete_inputs(starting_address, quantity, sock):
    """ Send read_discrete_inputs over socket. """
    msg = get_json_rpc_message('read_discrete_inputs',
                               {'starting_address': starting_address,
                                'quantity': quantity})
    return send_request(msg, sock)


def read_holding_registers(starting_address, quantity, sock):
    """ Send read_coils over socket. """
    msg = get_json_rpc_message('read_holding_registers',
                               {'starting_address': starting_address,
                                'quantity': quantity})
    return send_request(msg, sock)


def read_input_registers(starting_address, quantity, sock):
    """ Send read_input_registers over socket. """
    msg = get_json_rpc_message('read_input_registers',
                               {'starting_address': starting_address,
                                'quantity': quantity})
    return send_request(msg, sock)


def write_single_coil(address, value, sock):
    """ Send write_single_coil request over socket. """
    msg = get_json_rpc_message('write_single_coil', {'address': address,
                                                     'value': value})
    return send_request(msg, sock)


def write_single_register(address, value, sock):
    """ Send write_single_register request over socket. """
    msg = get_json_rpc_message('write_single_register', {'address': address,
                                                         'value': value})
    return send_request(msg, sock)


def write_multiple_coils(starting_address, values, sock):
    """ Send write_multiple_coils request over socket. """
    msg = get_json_rpc_message('write_multiple_coils',
                               {'starting_address': starting_address,
                                'values': values})

    return send_request(msg, sock)


def write_multiple_registers(starting_address, values, sock):
    """ Send write_multiple_registers request over socket. """
    msg = get_json_rpc_message('write_multiple_registers',
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


def test_read_discrete_inputs(running_server):
    """ Test following Modbus methods:
    * methods read_discrete_inputs, function code 02.
    """
    # Use read_discrete_input (function code 02) to read discrete inputs 0 and
    # 1.
    sock = get_socket(running_server.server_address)
    msg, resp = read_discrete_inputs(starting_address=0, quantity=2,
                                     sock=sock)
    assert json.loads(resp) == get_expected_response(msg, [1, 0])


def test_read_analog_inputs(running_server):
    """ Test following Modbus methods:
    * methods read_discrete_inputs, function code 04.
    """
    # Use read_input_registers (function code 02) to read input registers 0 and
    # 1.
    sock = get_socket(running_server.server_address)
    msg, resp = read_input_registers(starting_address=0, quantity=2,
                                     sock=sock)
    assert json.loads(resp) == get_expected_response(msg, [1337, 2890])


def test_read_and_write_holding_registers(running_server):
    """ Test following Modbus methods:
    * methods read_holding_registers, function code 03
    * write_single_register, function code 06
    * write_multiple_registers, function code 16
    """
    # First, use write_single_register (function code 06) to write 1337 to
    # register 100.
    sock = get_socket(running_server.server_address)
    msg, resp = write_single_register(address=100, value=1337, sock=sock)
    assert json.loads(resp) == get_expected_response(msg, [100, 1337])

    # Use read_coils (function code 01) to read coil 100.
    sock = get_socket(running_server.server_address)
    msg, resp = read_holding_registers(starting_address=100, quantity=1,
                                       sock=sock)
    assert json.loads(resp) == get_expected_response(msg, [1337])

    # Now, use write_multiple_registers (function code 16) to write 0 to
    # register 100 and 2674 to coil 101.
    sock = get_socket(running_server.server_address)
    msg, resp = write_multiple_registers(starting_address=100,
                                         values=[0, 2674], sock=sock)
    assert json.loads(resp) == get_expected_response(msg, [100, 2])

    # Read registers 100 and 101 again to verify previous write requests was
    # succesful.
    sock = get_socket(running_server.server_address)
    msg, resp = read_holding_registers(starting_address=100, quantity=2,
                                       sock=sock)
    assert json.loads(resp) == get_expected_response(msg, [0, 2674])


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

    # Read coils 100 and 101 again to verify previous write requests was
    # succesful.
    sock = get_socket(running_server.server_address)
    msg, resp = read_coils(starting_address=100, quantity=2, sock=sock)
    assert json.loads(resp) == get_expected_response(msg, [0, 1])
