import socket
import json
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


class TestDispatcher():

    def test_read_coils(self, running_server):
        sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        sock.connect(running_server.server_address)

        msg = get_json_rpc_message('read_coils', 100, 1)
        sock.sendall(msg)

        resp = sock.recv(1024)
        sock.close()

        assert json.loads(resp) == get_expected_response(msg, [0])
