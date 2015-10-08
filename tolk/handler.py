""" Handler for dispatching incoming requests to
:class:`tolk.Dispatcher`.

"""
import socket
import errno
from logbook import Logger
from SocketServer import BaseRequestHandler

log = Logger(__name__)


class Handler(BaseRequestHandler):
    """ Handler for delegating incoming requests to :class:`Dispatcher`
    instance and return its response to client.

    :class:`Handler` is a subclass of :class:`SocketServer.BaseRequestHandler`
    and can be used in combination with a :class:`SocketServer.BaseServer`
    instance. This server must have an attribute :attr:`dispatcher` with an
    instance of :class:`Dispatcher`.

    Below you find a few lines of code to create a server listening on a Unix
    Domain Socket for JSON-RPC requests. These requests are delegated to a
    :class:`Dispatcher` instance which in turn sends Modbus request over RTU
    using a serial port::

        from modbus_tk.modbus_tcp import TcpMaster
        from SocketServer import UnixStreamServer

        from tolk import Dispatcher, Handler

        modbus_master = TcpMaster('localhost', 502)
        dispatcher = Dispatcher(modbus_master)

        server = UnixStreamServer('/tmp/tolk.sock', Handler)
        server.dispatcher = dispatcher

        server.serve_forever()

    """
    def handle(self):
        """ Direct incoming requests to server's dispatcher and return response
        back to client.
        """
        self.data = self.request.recv(1024).strip()
        log.debug('<-- {}'.format(self.data))

        resp = self.server.dispatcher.call(self.data)
        log.debug('--> {}'.format(resp))

        try:
            self.request.sendall(resp)
        except socket.error as e:

            # Catches broken pipe errors, errno 32. This is when client
            # terminates connection, but server still tries to send data to
            # client.
            if e.errno == errno.EPIPE:
                log.error('[Errno {}]: Handler could not send response to '
                          'client.'.format(errno.EPIP))

                return
            raise
