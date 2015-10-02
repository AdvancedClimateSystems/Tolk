import pytest
from threading import Thread
from SocketServer import UnixStreamServer

from tolk import Handler, Dispatcher


@pytest.fixture
def dispatcher():
    """ Return Dispatcher instance. """
    return Dispatcher(None)


@pytest.fixture
def server(dispatcher, monkeypatch, tmpdir):
    """ Return UnixStreamServer combined with Handler and a Dispatcher
    instance. """
    def mock_call(*args, **kwargs):
        return 'test response'

    socket_path = tmpdir.join('test_tolk_socket').strpath
    monkeypatch.setattr(dispatcher, 'call', mock_call)

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
