# Tolk
Tolk exposes a JSON-RPC API to talk Modbus over RTU and is written in Python.

## Quickstart
Tolk ships with 3 scripts to help during development and testing:

* [modbus_tcp_slave][modbus_tcp_slave.py]: Create a Modbus slave listening at a
    port.
* [tolk_server][tolk_server.py]: Start Tolk server listening at Unix Domain Socket for
    JSON-RPC request to proxy to the Modbus slave.
* [json_rpc_client][json_rpc_client.py]: Send JSON-RPC requests to Tolk server.

Start the Modbus slave...

```shell
$ ./scripts/modbus_tcp_slave --port=502
[2015-10-03 11:02:47.796836] INFO: __main__: Add analog inputs data block from register 0 to 99 on slave 1
[2015-10-03 11:02:47.797037] INFO: __main__: Add discrete inputs data block from register 0 to 99 on slave 1
[2015-10-03 11:02:47.797176] INFO: __main__: Add coils data block from register 100 to 199 on slave 1
[2015-10-03 11:02:47.797305] INFO: __main__: Add holding registers block from register 100 to 199 on slave 1
[2015-10-03 11:02:47.797671] INFO: __main__: TcpServer started listening at port 1025.
```

...and the Tolk server...

```shell
$ ./scripts/tolk_server.py --modbus-port=1025 --socket=/tmp/tolk.sock
[2015-10-03 11:04:05.661391] INFO: __main__: Start Tolk listening at /tmp/tolk.sock.
```

... and send requests:

```shell
./scripts/json_rpc_client.py read_coils 100 1 --socket=/tmp/tolk.sock
{
    "id": 203448389051845515226734861262256644311,
    "jsonrpc": "2.0",
    "result": [
        0
    ]
}
```

## Tests
Tolk uses [Pytest][pytest]. Running the test stuite is easy:

```shell
$ docker-compose run tests
```

## Documentation
Documentation resides in docs/ and is written using Sphinx. The source of
documentation is located at docs/source. The builded docs are written to
docs/build.

```shell
$ docker-compose run docs
```
The generated docs are stored in `docs/build/`.

## License
This software is licensed under [Mozila Public License][mpl].
&copy; 2015 [Advanced Climate Systems][acs].

[acs]: http://advancedclimate.nl
[docker-compose]: docker-compose.yml
[json_rpc_client.py]: scripts/json_rpc_client.py
[modbus_tcp_slave.py]: scripts/modbus_tcp_slave.py
[mpl]: LICENSE
[pytest]: http://pytest.org/latest/
[sphinx]: http://sphinx-doc.org/
[tolk_server.py]: scripts/tolk.py
