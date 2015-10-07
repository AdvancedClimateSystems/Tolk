from pyjsonrpc import JsonRpc, rpcmethod
from modbus_tk.defines import (READ_COILS, READ_DISCRETE_INPUTS,
                               READ_HOLDING_REGISTERS, READ_INPUT_REGISTERS,
                               WRITE_SINGLE_COIL, WRITE_SINGLE_REGISTER,
                               WRITE_MULTIPLE_COILS, WRITE_MULTIPLE_REGISTERS)


class Dispatcher(JsonRpc):

    def __init__(self, modbus_master):
        self.modbus_master = modbus_master

        super(JsonRpc, self).__init__()

    @rpcmethod
    def read_coils(self, starting_address, quantity, slave_id=1):
        """ Execute Modbus function code 01: read status of coils.

        :param starting_address: Number of starting address.
        :param quantity: Number of coils to read.
        :param slave: Number with Slave id, default 1.
        """
        return self.modbus_master.execute(int(slave_id), READ_COILS,
                                          int(starting_address),
                                          int(quantity))

    @rpcmethod
    def read_discrete_inputs(self, starting_address, quantity,
                             slave_id=1):
        """ Execute Modbus function code 02: read status of discreate inputs.

        :param starting_address: Number of starting address.
        :param quantity: Number of discrete inputs to read.
        :param slave: Number with Slave id, default 1.
        """
        return self.modbus_master.execute(int(slave_id), READ_DISCRETE_INPUTS,
                                          int(starting_address),
                                          int(quantity))

    @rpcmethod
    def read_holding_registers(self, starting_address, quantity,
                               slave_id=1):
        """ Execute Modbus function code 03: read contents of contiguous block
        of holding registers.

        :param starting_address: Number of starting address.
        :param quantity: Number of holding registers to read.
        :param slave: Number with Slave id, default 1.
        """
        return self.modbus_master.execute(int(slave_id),
                                          READ_HOLDING_REGISTERS,
                                          int(starting_address), int(quantity))

    @rpcmethod
    def read_input_registers(self, starting_address, quantity,
                             slave_id=1):
        """ Execute Modbus function code 04: read contents of contiguous block
        of input registers.

        :param starting_address: Number of starting address.
        :param quantity: Number of input registers to read.
        :param slave: Number with Slave id, default 1.
        """
        return self.modbus_master.execute(int(slave_id),
                                          READ_INPUT_REGISTERS,
                                          int(starting_address), int(quantity))

    @rpcmethod
    def write_single_coil(self, address, value, slave_id=1):
        """ Execute Modbus function code 05: write value to single coil.

        :param address: Address of coil.
        :param value: Value to write to coil.
        :param slave: Number with Slave id, default 1.
        """
        return self.modbus_master.execute(int(slave_id),
                                          WRITE_SINGLE_COIL, int(address),
                                          output_value=int(value))

    @rpcmethod
    def write_single_register(self, address, value, slave_id=1):
        """ Execute Modbus function code 06: write value to single holding
        register.

        :param address: Address of holding register.
        :param value: Value to write to holding register.
        :param slave: Number with Slave id, default 1.
        """
        return self.modbus_master.execute(int(slave_id),
                                          WRITE_SINGLE_REGISTER, int(address),
                                          output_value=int(value))

    @rpcmethod
    def write_multiple_coils(self, starting_address, values,
                             slave_id=1):
        """ Execute Modbus function code 15: write sequence of values to a
        contiguous block of coils.

        .. note:: This method doesn't follow the interface as described in the
            Modbus specification. The specification describes 2 extra
            'parameters': quantity of outputs and byte count. Tolk will derive
            them from paramater `values`.

        :param starting_address: Number of starting address.
        :param values: List with values.
        :param slave: Number with Slave id, default 1.
        """
        values = [int(v) for v in values]
        return self.modbus_master.execute(int(slave_id),
                                          WRITE_MULTIPLE_COILS,
                                          int(starting_address),
                                          output_value=values)

    @rpcmethod
    def write_multiple_registers(self, starting_address, values,
                                 slave_id=1):
        """ Execute Modbus function code 16: write sequence of values to a
        contiguous block of holding registers.

        .. note:: This method doesn't follow the interface as described in the
            Modbus specification. The specification describes 2 extra
            'parameters': quantity of outputs and byte count. Tolk will derive
            them from paramater `values`.

        :param starting_address: Number of starting address.
        :param values: List with values to write.
        :param slave: Number with Slave id, default 1.
        """
        values = [int(v) for v in values]
        return self.modbus_master.execute(int(slave_id),
                                          WRITE_MULTIPLE_REGISTERS,
                                          int(starting_address),
                                          output_value=values)
