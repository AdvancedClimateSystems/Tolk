import pytest
import socket
from threading import Thread
from SocketServer import UnixStreamServer
from modbus_tk.defines import (ANALOG_INPUTS, DISCRETE_INPUTS, COILS,
                               HOLDING_REGISTERS)
from modbus_tk.modbus_tcp import TcpMaster, TcpServer

from tolk import Handler, Dispatcher


@pytest.yield_fixture
def modbus_server():
    modbus_server = TcpServer(port=7632)

    slave = modbus_server.add_slave(1)

    slave.add_block(0, ANALOG_INPUTS, 0, 100)
    slave.add_block(1, DISCRETE_INPUTS, 0, 100)
    slave.add_block(2, COILS, 100, 100)
    slave.add_block(3, HOLDING_REGISTERS, 100, 100)

    modbus_server.start()

    yield modbus_server

    modbus_server.stop()


@pytest.fixture
def modbus_master(modbus_server):
    """ Return an instance of TcpMaster with mocked attribute `execute`. This
    method always returns [0].
    """
    _, port = modbus_server._sa
    modbus_master = TcpMaster(port=port)

    return modbus_master


@pytest.fixture
def dispatcher(modbus_master):
    """ Return Dispatcher instance. """
    return Dispatcher(modbus_master)


@pytest.fixture
def server(dispatcher, tmpdir):
    """ Return UnixStreamServer combined with Handler and a Dispatcher
    instance. """

    socket_path = tmpdir.join('test_tolk_socket').strpath

    s = UnixStreamServer(socket_path, Handler)
    s.dispatcher = dispatcher

    return s


@pytest.yield_fixture
def running_server(server):
    """ Start server in a thread, yield instance and stop the server after
    yielding. """
    start_thread = Thread(target=server.serve_forever)
    start_thread.start()

    yield server

    server.shutdown()


@pytest.yield_fixture
def sock(running_server):
    """ Return socket instance connected to Tolk server. """
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    sock.connect(running_server.server_address)

    yield sock

    sock.close()
