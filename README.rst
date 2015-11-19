.. image::  https://travis-ci.org/AdvancedClimateSystems/Tolk.svg?branch=master
    :target: https://travis-ci.org/AdvancedClimateSystems/Tolk
.. image:: https://coveralls.io/repos/AdvancedClimateSystems/Tolk/badge.svg?branch=master&service=github
    :target: https://coveralls.io/github/AdvancedClimateSystems/Tolk?branch=master
.. image:: https://img.shields.io/pypi/v/tolk.svg
    :target: https://pypi.python.org/pypi/Tolk/

Tolk
====

Tolk exposes a JSON-RPC API to talk Modbus over RTU or TCP and is written in
Python. The source can be found on GitHub_. Documentation is available at
`Read the Docs`_.

Quickstart
----------
Below you can find sample code how to start Tolk listening at a Unix Domain
Socket for JSON-RPC request. Tolk will delegate the requests via the
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

License
-------

This software is licensed under `Mozilla Public License`_.  &copy; 2015
`Advanced Climate Systems`_.

.. External References:
.. _Advanced Climate Systems: http://advancedclimate.nl
.. _GitHub: https://github.com/AdvancedClimateSystems/Tolk
.. _modbus_tcp_slave.py: scripts/modbus_tcp_slave.py
.. _Mozilla Public License: LICENSE
.. _pytest: http://pytest.org/latest/
.. _json_rpc_client.py: scripts/json_rpc_client.py
.. _tolk_server.py: scripts/tolk.py
.. _Read the Docs: https://tolk.readthedocs.org/en/latest/
