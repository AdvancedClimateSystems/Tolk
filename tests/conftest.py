import pytest
from threading import Thread
from modbus_tk.modbus_tcp import TcpMaster
from SocketServer import UnixStreamServer

from tolk import Handler, Dispatcher


@pytest.fixture
def modbus_master():
    """ Return an instance of TcpMaster with mocked attribute `execute`. This
    method always returns [0].
    """
    modbus_master = TcpMaster()

    def mock_execute(*args, **kwargs):
        return [0]

    modbus_master.execute = mock_execute
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
