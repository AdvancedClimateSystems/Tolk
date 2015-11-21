.. _usage:

Usage
=====

Dispatcher
----------

Tolk is a JSON-RPC proxy for doing Modbus request over RTU or TCP.
:class:`tolk.Dispatcher` implements the JSON-RPC API. The
:class:`tolk.Dispatcher` needs a :class:`modbus_tk.modbus.Master` to dispatch
incoming requests to.

.. code:: python

    >>> import json
    >>> from modbus_tk.modbus_tcp import TcpMaster
    >>> from tolk import Dispatcher
    >>> modbus_master = TcpMaster('localhost', 502)
    >>> dispatcher = Dispatcher(modbus_master)
    >>> dispatcher.call(json.dumps({
            'jsonrpc': '2.0',
            'method': 'read_holding_registers',
            'params': {
                'starting_address': 100,
                'quantity': 2,
            },
            'id': 1
        }
    '{"jsonrpc": "2.0", "id": 1, "result": [1337, 2345]}'


Handler
-------

:class:`tolk.Handler` is a subclass of :class:`SocketServer.BaseRequestHandler`.
This class can delegate incomming JSON-RPC requests on a Unix Domain Socket or
a TCP socket to an instance of :class:`tolk.Dispatcher`.

.. code:: python

    from modbus_tk.modbus_tcp import TcpMaster
    from SocketServer import UnixStreamServer

    from tolk import Dispatcher, Handler

    modbus_master = TcpMaster('localhost', 502)
    dispatcher = Dispatcher(modbus_master)

    server = UnixStreamServer('/tmp/tolk.sock', Handler)
    # Bind the dispatcher on the server.
    server.dispatcher = dispatcher

    server.serve_forever()

Scripts
-------
Tolk ships with 3 scripts to help during development and testing:

* :ref:`modbus_tcp_slave`: Create a Modbus slave listening at a port.
* :ref:`tolk_server`: Start Tolk server listening at Unix Domain Socket for
  JSON-RPC request to proxy to the Modbus slave.
* :ref:`json_rpc_client`: Send JSON-RPC requests to Tolk server.

Section :ref:`scripts` tells more about these scripts.

Start the Modbus slave...::

    $ ./scripts/modbus_tcp_slave --port=1025
    [2015-10-03 11:02:47.796836] INFO: __main__: Add analog inputs data block from register 0 to 99 on slave 1
    [2015-10-03 11:02:47.797037] INFO: __main__: Add discrete inputs data block from register 0 to 99 on slave 1
    [2015-10-03 11:02:47.797176] INFO: __main__: Add coils data block from register 100 to 199 on slave 1
    [2015-10-03 11:02:47.797305] INFO: __main__: Add holding registers block from register 100 to 199 on slave 1
    [2015-10-03 11:02:47.797671] INFO: __main__: TcpServer started listening at port 1025.

...and the Tolk server...::

    $ ./scripts/tolk_server.py --modbus-port=1025 --socket=/tmp/tolk.sock
    [2015-10-03 11:04:05.661391] INFO: __main__: Start Tolk listening at /tmp/tolk.sock.

... and send requests::

    $ ./scripts/json_rpc_client.py read_coils 100 1 --socket=/tmp/tolk.sock
    {
        "id": 203448389051845515226734861262256644311,
        "jsonrpc": "2.0",
        "result": [
            0k
        ]
    }
