import pytest
from mock import Mock
from modbus_tk.modbus import ModbusError
from tolk.exceptions import (json_rpc_error, IllegalFunction,
                             IllegalDataAddress, IllegalDataValue,
                             SlaveDeviceFailure, CommandAcknowledge,
                             SlaveDeviceBusy, NegativeAcknowlegde,
                             MemoryParityError, GateWayPathUnavailable,
                             GatewayTargetDeviceFailedToRespond)


@pytest.mark.parametrize('modbus_code,json_rpc_exception,expected', [
    (1, IllegalFunction, 'JsonRpcError(-32001): Function code is not valid.'),
    (2, IllegalDataAddress, 'JsonRpcError(-32002): Data address is not valid.'),
    (3, IllegalDataValue, 'JsonRpcError(-32003): Data value is not valid.'),
    (4, SlaveDeviceFailure, 'JsonRpcError(-32004): Slave device could not '
                            'perform requested action.'),
    (5, CommandAcknowledge, 'JsonRpcError(-32005): Slave device has accepted '
                            'the request and is processing it, but a long '
                            'duration of time will be required to do so. '
                            'This response is returned to prevent a timeout '
                            'error from occurring in the master.'),
    (6, SlaveDeviceBusy, 'JsonRpcError(-32006): Slave device is busy.'),
    (7, NegativeAcknowlegde, 'JsonRpcError(-32007): Slave device cannot perform '
                             'the program function received in the query.'),
    (8, MemoryParityError, 'JsonRpcError(-32008): Slave device failed to read '
                           'extended memory or record file.'),
    (10, GateWayPathUnavailable, 'JsonRpcError(-32010): Gateway is unable to '
                                 'allocate an internal communication path from '
                                 'the input port to the output port.'),
    (11, GatewayTargetDeviceFailedToRespond, 'JsonRpcError(-32011): No response '
                                             'obtained from the target device.')
])
def test_raise_modbus_json_rpc_error(modbus_code, json_rpc_exception, expected):
    func = Mock(side_effect=ModbusError(modbus_code))
    func.__name__ = 'function_name'
    decorated_func = json_rpc_error(func)

    with pytest.raises(json_rpc_exception) as exinfo:
        decorated_func()

    assert str(exinfo.value) == expected
