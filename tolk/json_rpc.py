from modbus_tk.defines import (READ_COILS, READ_DISCRETE_INPUTS,
                               READ_HOLDING_REGISTERS, READ_INPUT_REGISTERS,
                               WRITE_SINGLE_COIL, WRITE_SINGLE_REGISTER,
                               WRITE_MULTIPLE_COILS, WRITE_MULTIPLE_REGISTERS)
from pyjsonrpc import JsonRpc, rpcmethod
from tolk.exceptions import json_rpc_error


class Dispatcher(JsonRpc):
    def __init__(self, modbus_master):
        self.modbus_master = modbus_master

        super(JsonRpc, self).__init__()

    @rpcmethod
    @json_rpc_error
    def read_coils(self, starting_address, quantity, slave_id=1):
        """ Execute Modbus function code 01: read status of coils.

        :param starting_address: Number of starting address.
        :param quantity: Number of coils to read.
        :param slave_id: Number with Slave id, default 1.
        :returns: JSON-RPC response containing the status of coils on success JSON-RPC error on failure.

        **Example request:**

        .. sourcecode:: json

            {
                "params":{
                    "starting_address":100,
                    "quantity":2,
                    "slave_id":1
                },
                "jsonrpc":"2.0",
                "method":"read_coils",
                "id":1
            }

        **Example response:**

        .. sourcecode:: json

            {
                "jsonrpc":"2.0",
                "id":1,
                "result":[
                    0,
                    1
                ]
            }
        """
        return self.modbus_master.execute(int(slave_id), READ_COILS,
                                          int(starting_address),
                                          int(quantity))

    @rpcmethod
    @json_rpc_error
    def read_discrete_inputs(self, starting_address, quantity, slave_id=1):
        """ Execute Modbus function code 02: read status of discrete inputs.

        :param starting_address: Number of starting address.
        :param quantity: Number of discrete inputs to read.
        :param slave_id: Number with Slave id, default 1.
        :returns: JSON-RPC response containing the status of discrete inputs
        on success or JSON-RPC error on failure.

        **Example request:**

        .. sourcecode:: json

            {
                "params":{
                    "starting_address":0,
                    "quantity":2,
                    "slave_id":1
                },
                "jsonrpc":"2.0",
                "method":"read_discrete_inputs",
                "id":1
            }

        **Example response:**

        .. sourcecode:: json

            {
                "jsonrpc":"2.0",
                "id":1,
                "result":[
                    0,
                    1,
                ]
            }
        """
        return self.modbus_master.execute(int(slave_id), READ_DISCRETE_INPUTS,
                                          int(starting_address),
                                          int(quantity))

    @rpcmethod
    @json_rpc_error
    def read_holding_registers(self, starting_address, quantity, slave_id=1):
        """ Execute Modbus function code 03: read contents of contiguous block
        of holding registers.

        :param starting_address: Number of starting address.
        :param quantity: Number of holding registers to read.
        :param slave_id: Number with Slave id, default 1.
        :returns: JSON-RPC response with the contents of holding registers
        on success or JSON-RPC error on failure.

        **Example request:**

        .. sourcecode:: json

            {
                "params":{
                    "starting_address":100,
                    "quantity":2,
                    "slave_id":1
                },
                "jsonrpc":"2.0",
                "method":"read_holding_registers",
                "id":1
            }

        **Example response:**

        .. sourcecode:: json

            {
                "jsonrpc":"2.0",
                "id":1,
                "result":[
                    1234,
                    32433,
                ]
            }
        """
        return self.modbus_master.execute(int(slave_id), READ_HOLDING_REGISTERS,
                                          int(starting_address),
                                          int(quantity))

    @rpcmethod
    @json_rpc_error
    def read_input_registers(self, starting_address, quantity, slave_id=1):
        """ Execute Modbus function code 04: read contents of contiguous block
        of input registers.

        :param starting_address: Number of starting address.
        :param quantity: Number of input registers to read.
        :param slave_id: Number with Slave id, default 1.
        :returns: JSON-RPC response with the contents of input registers
        on success or JSON-RPC error on failure.

        **Example request:**

        .. sourcecode:: json

            {
                "params":{
                    "starting_address":100,
                    "quantity":2,
                    "slave_id":1
                },
                "jsonrpc":"2.0",
                "method":"read_input_registers",
                "id":1
            }

        **Example response:**

        .. sourcecode:: json

            {
                "jsonrpc":"2.0",
                "id":1,
                "result":[
                    1234,
                    32433,
                ]
            }
        """
        return self.modbus_master.execute(int(slave_id), READ_INPUT_REGISTERS,
                                          int(starting_address),
                                          int(quantity))

    @rpcmethod
    @json_rpc_error
    def write_single_coil(self, address, value, slave_id=1):
        """ Execute Modbus function code 05: write value to single coil.

        :param address: Address of coil.
        :param value: Value to write to coil.
        :param slave_id: Number with Slave id, default 1.
        :returns: JSON-RPC response containing the address and value that has been written.

        **Example request:**

        .. sourcecode:: json

            {
                "params":{
                    "starting_address":100,
                    "value":1,
                    "slave_id":1
                },
                "jsonrpc":"2.0",
                "method":"write_single_coil",
                "id":1
            }

        **Example response:**

        .. sourcecode:: json

            {
                "jsonrpc":"2.0",
                "id":1,
                "result":[
                    100,
                    65280,
                ]
            }
        """
        return self.modbus_master.execute(int(slave_id), WRITE_SINGLE_COIL,
                                          int(address), output_value=int(value))

    @rpcmethod
    @json_rpc_error
    def write_single_register(self, address, value, slave_id=1):
        """ Execute Modbus function code 06: write value to single holding
        register.

        :param address: Address of holding register.
        :param value: Value to write to holding register.
        :param slave_id: Number with Slave id, default 1.
        :returns: JSON-RPC response containing the address and the value that has been written.

        **Example request:**

        .. sourcecode:: json

            {
                "params":{
                    "starting_address":100,
                    "value":1234,
                    "slave_id":1
                },
                "jsonrpc":"2.0",
                "method":"write_single_register",
                "id":1
            }

        **Example response:**

        .. sourcecode:: json

            {
                "jsonrpc":"2.0",
                "id":1,
                "result":[
                    100,
                    1234,
                ]
            }
        """
        return self.modbus_master.execute(int(slave_id),
                                          WRITE_SINGLE_REGISTER, int(address),
                                          output_value=int(value))

    @rpcmethod
    @json_rpc_error
    def write_multiple_coils(self, starting_address, values, slave_id=1):
        """ Execute Modbus function code 15: write sequence of values to a
        contiguous block of coils.

        .. note:: This method doesn't follow the interface as described in the
            Modbus specification. The specification describes 2 extra
            'parameters': quantity of outputs and byte count. Tolk will derive
            them from parameter `values`.

        :param starting_address: Number of starting address.
        :param values: List with values.
        :param slave_id: Number with Slave id, default 1.
        :returns: JSON-RPC response containing the address and the number of coils that has been written.

        **Example request:**

        .. sourcecode:: json

            {
                "params":{
                    "starting_address":100,
                    "value": [1, 0, 1, 0],
                    "slave_id":1
                },
                "jsonrpc":"2.0",
                "method":"write_multiple_coils",
                "id":1
            }

        **Example response:**

        .. sourcecode:: json

            {
                "jsonrpc":"2.0",
                "id":1,
                "result":[
                    100,
                    4,
                ]
            }
        """
        values = [int(v) for v in values]
        return self.modbus_master.execute(int(slave_id),
                                          WRITE_MULTIPLE_COILS,
                                          int(starting_address),
                                          output_value=values)

    @rpcmethod
    @json_rpc_error
    def write_multiple_registers(self, starting_address, values, slave_id=1):
        """ Execute Modbus function code 16: write sequence of values to a
        contiguous block of holding registers.

        .. note:: This method doesn't follow the interface as described in the
            Modbus specification. The specification describes 2 extra
            'parameters': quantity of outputs and byte count. Tolk will derive
            them from parameter `values`.

        :param starting_address: Number of starting address.
        :param values: List with values to write.
        :param slave_id: Number with Slave id, default 1.
        :returns: JSON-RPC response containing the address and the number of values that has been written.

        **Example request:**

        .. sourcecode:: json

            {
                "params":{
                    "starting_address":100,
                    "value": [1234, 5678, 9012, 3456],
                    "slave_id":1
                },
                "jsonrpc":"2.0",
                "method":"write_multiple_registers",
                "id":1
            }

        **Example response:**

        .. sourcecode:: json

            {
                "jsonrpc":"2.0",
                "id":1,
                "result":[
                    100,
                    4,
                ]
            }
        """
        values = [int(v) for v in values]
        return self.modbus_master.execute(int(slave_id),
                                          WRITE_MULTIPLE_REGISTERS,
                                          int(starting_address),
                                          output_value=values)
