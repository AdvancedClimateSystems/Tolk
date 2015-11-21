from functools import wraps

from modbus_tk.modbus import ModbusError
from pyjsonrpc.rpcerror import jsonrpcerrors, JsonRpcError

modbus_mapping = {}


def json_rpc_error(func):
    """ Wraps a function and raises a JSON RPC error when a ModbusError has
    been excepted::

        @json_rpc_error()
        def modbus_request(modbus_master, slave_id, function_code,
                           starting_address, quantity):

        modbus_master.execute(int(slave_id), function_code,
                              int(starting_address),
                              int(quantity))

    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ModbusError as e:
            raise modbus_mapping[e.get_exception_code()]
    return wrapper


class IllegalFunction(JsonRpcError):
    code = -32001
    message = 'Function code is not valid.'


jsonrpcerrors[IllegalFunction.code] = IllegalFunction
modbus_mapping[1] = IllegalFunction


class IllegalDataAddress(JsonRpcError):
    code = -32002
    message = 'Data address is not valid.'


jsonrpcerrors[IllegalDataAddress.code] = IllegalDataAddress
modbus_mapping[2] = IllegalDataAddress


class IllegalDataValue(JsonRpcError):
    code = -32003
    message = 'Data value is not valid.'


jsonrpcerrors[IllegalDataValue.code] = IllegalDataValue
modbus_mapping[3] = IllegalDataValue


class SlaveDeviceFailure(JsonRpcError):
    code = -32004
    message = 'Slave device could not perform requested action.'


jsonrpcerrors[SlaveDeviceFailure.code] = SlaveDeviceFailure
modbus_mapping[4] = SlaveDeviceFailure


class CommandAcknowledge(JsonRpcError):
    code = -32005
    message = 'Slave device has accepted the request and is ' \
              'processing it, but a long duration of time will be required to ' \
              'do so. This response is returned to prevent a timeout error ' \
              'from occurring in the master.'


jsonrpcerrors[CommandAcknowledge.code] = CommandAcknowledge
modbus_mapping[5] = CommandAcknowledge


class SlaveDeviceBusy(JsonRpcError):
    code = -32006
    message = 'Slave device is busy.'


jsonrpcerrors[SlaveDeviceBusy.code] = SlaveDeviceBusy
modbus_mapping[6] = SlaveDeviceBusy


class NegativeAcknowlegde(JsonRpcError):
    code = -32007
    message = 'Slave device cannot perform the program function received in the ' \
              'query.'


jsonrpcerrors[NegativeAcknowlegde.code] = NegativeAcknowlegde
modbus_mapping[7] = NegativeAcknowlegde


class MemoryParityError(JsonRpcError):
    code = -32008
    message = 'Slave device failed to read extended memory or record file.'


jsonrpcerrors[MemoryParityError.code] = MemoryParityError
modbus_mapping[8] = MemoryParityError


class GateWayPathUnavailable(JsonRpcError):
    code = -32010
    message = 'Gateway is unable to allocate an internal communication path from ' \
              'the input port to the output port.'


jsonrpcerrors[GateWayPathUnavailable.code] = GateWayPathUnavailable
modbus_mapping[10] = GateWayPathUnavailable


class GatewayTargetDeviceFailedToRespond(JsonRpcError):
    code = -32011
    message = 'No response obtained from the target device.'


jsonrpcerrors[GatewayTargetDeviceFailedToRespond.code] = GatewayTargetDeviceFailedToRespond
modbus_mapping[11] = GatewayTargetDeviceFailedToRespond
