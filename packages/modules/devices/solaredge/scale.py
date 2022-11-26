import logging
import math
from typing import List

from modules.common.modbus import ModbusDataType, ModbusTcpClient_, Number

log = logging.getLogger(__name__)

# Registers that are not applicable to a meter class return the unsupported value. (e.g. Single Phase
# meters will support only summary and phase A values):

UINT16_UNSUPPORTED = 0xFFFF


def scale_registers(registers: List[Number]) -> List[float]:
    log.debug("Registers %s, Scale %s", registers[:-1],  registers[-1])
    scale = math.pow(10, registers[-1])
    return [register * scale if register != UINT16_UNSUPPORTED else 0 for register in registers[:-1]]


def create_scaled_reader(client: ModbusTcpClient_, modbus_id: int, type: ModbusDataType):
    def scaled_reader(address: int, count: int):
        return scale_registers(
            client.read_holding_registers(address, [type] * count + [ModbusDataType.INT_16], unit=modbus_id)
        )

    return scaled_reader
