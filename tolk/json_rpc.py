from pyjsonrpc import JsonRpc, rpcmethod
from modbus_tk.defines import (READ_COILS, READ_DISCRETE_INPUTS,
                               READ_HOLDING_REGISTERS)


class Dispatcher(JsonRpc):

    def __init__(self, modbus_master):
        self.modbus_master = modbus_master

        super(JsonRpc, self).__init__()

    @rpcmethod
    def read_coils(self, starting_address, quantity, port=1, slave_id=1):
        """ Execute Modbus function code 01: read status of coils.

        :param starting_address: Number of starting address.
        :param quantity: Number of coils to read.
        :param port: Number of serial port, default 1.
        :param slave: Number with Slave id, default 1.
        """
        return self.modbus_master.execute(int(slave_id), READ_COILS,
                                          int(starting_address),
                                          int(quantity), int(port))

    @rpcmethod
    def read_discrete_inputs(self, starting_address, quantity, port=1,
                             slave_id=1):
        """ Execute Modbus function code 02: read status of discreate inputs.

        :param starting_address: Number of starting address.
        :param quantity: Number of discrete inputs to read.
        :param port: Number of serial port, default 1.
        :param slave: Number with Slave id, default 1.
        """
        return self.modbus_master.execute(int(slave_id), READ_DISCRETE_INPUTS,
                                          int(starting_address),
                                          int(quantity), int(port))

    @rpcmethod
    def read_holding_registers(self, starting_address, quantity, port=1,
                               slave_id=1):
        """ Execute Modbus function code 03: read contents of contiguous block of
        holding registers.

        :param starting_address: Number of starting address.
        :param quantity: Number of holding registers to read.
        :param port: Number of serial port, default 1.
        :param slave: Number with Slave id, default 1.
        """
        return self.modbus_master.execute(int(slave_id),
                                          READ_HOLDING_REGISTERS,
                                          int(starting_address), int(quantity),
                                          int(port))

    @rpcmethod
    def read_input_registers(self, starting_address, quantity, port=1,
                             slave_id=1):
        """ Execute Modbus function code 04: read contents of contiguous block of
        input registers.

        :param starting_address: Number of starting address.
        :param quantity: Number of input registers to read.
        :param port: Number of serial port, default 1.
        :param slave: Number with Slave id, default 1.
        """
        pass

    @rpcmethod
    def write_single_coil(self, address, value, port=1, slave_id=1):
        """ Execute Modbus function code 05: write value to single coil.

        :param address: Address of coil.
        :param value: Value to write to coil.
        :param port: Number of serial port, default 1.
        :param slave: Number with Slave id, default 1.
        """
        pass

    @rpcmethod
    def write_single_register(self, address, value, port=1, slave_id=1):
        """ Execute Modbus function code 06: write value to single holding
        register.

        :param address: Address of holding register.
        :param value: Value to write to holding register.
        :param port: Number of serial port, default 1.
        :param slave: Number with Slave id, default 1.
        """
        pass

    @rpcmethod
    def write_multiple_coils(self, starting_address, values, port=1,
                             slave_id=1):
        """ Execute Modbus function code 15: write sequence of values to a
        contiguous block of coils.

        .. note:: This method doesn't follow the interface as described in the
            Modbus specification. The specification describes 2 extra
            'parameters': quantity of outputs and byte count. Tolk will derive
            them from paramater `values`.

        :param starting_address: Number of starting address.
        :param values: List with values.
        :param port: Number of serial port, default 1.
        :param slave: Number with Slave id, default 1.
        """
        pass

    @rpcmethod
    def write_multiple_registers(self, starting_address, values, port=1,
                                 slave_id=1):
        """ Execute Modbus function code 16: write sequence of values to a
        contiguous block of holding registers.

        .. note:: This method doesn't follow the interface as described in the
            Modbus specification. The specification describes 2 extra
            'parameters': quantity of outputs and byte count. Tolk will derive
            them from paramater `values`.

        :param starting_address: Number of starting address.
        :param values: List with values to write.
        :param port: Number of serial port, default 1.
        :param slave: Number with Slave id, default 1.
        """
        pass
