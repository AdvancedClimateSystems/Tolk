import socket


def test_request_on_server(running_server):
    """ Test if Handler return expected response. """
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    sock.connect(running_server.server_address)
    sock.settimeout(5)

    sock.sendall('test request')
    resp = sock.recv(1024)

    assert resp == 'test response'

    sock.close()
