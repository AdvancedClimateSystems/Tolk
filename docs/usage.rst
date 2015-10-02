Usage
=====

.. code:: python
    
    import fcntl
    import struct
    from serial import Serial
    from modbus_tk.modbus_rtu import RtuMaster

    from tolk.server import Server, Handler
    from tolk.json_rpc import ModbusDispatcher

    serial_port = Serial()

    # Configure serial port to use RS485 interface.
    fh = serial_port.fileno()
    serial_rs485 = struct.pack('hhhhhhhh', 1, 0, 0, 0, 0, 0, 0, 0)
    fnctl.ioctl(fh, 0x542F, serial_port)

    modbus_master = RtuMaster(serial_port)
    dispatcher = Dispatcher()

    server = Server('/tmp/server', Handler, dispatcher=dispatcher)

    server
