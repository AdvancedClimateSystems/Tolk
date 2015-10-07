.. Tolk documentation master file, created by
   sphinx-quickstart on Wed Sep 30 13:15:07 2015.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Tolk
====

Tolk is a JSON-RPC proxy for doing Modbus, either over TCP or over RTU. Below
you can find sample code how to start Tolk listening at a Unix Domain Socket
for JSON-RPC request. Tolk will delegate the requests via the
:class:`Dispatcher` to the :class:`modbus_tk.modbus_tcp.TcpMaster` which in
turn will request a Modbus slave at `localhost:502`.

.. code:: python

    from modbus_tk.modbus_tcp import TcpMaster
    from SocketServer import UnixStreamServer

    from tolk import Dispatcher, Handler

    # The TcpMaster will fire requests to a Modbus slave at localhost:502.
    modbus_master = TcpMaster('localhost', 502)
    dispatcher = Dispatcher(modbus_master)

    server = UnixStreamServer('/tmp/tolk.sock', Handler)
    server.dispatcher = dispatcher

    server.serve_forever()

Tolk is completely open source and can be found on GitHub_.

Contents:
---------

.. toctree::
   :maxdepth: 2

   installation
   usage
   api
   scripts
   modules

.. External references:
.. _GitHub: https://github.com/AdvancedClimateSystems/Tolk
