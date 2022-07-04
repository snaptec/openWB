import math
from typing import List

from modules.common.modbus import Number

# Registers that are not applicable to a meter class return the unsupported value. (e.g. Single Phase
# meters will support only summary and phase A values):

UINT16_UNSUPPORTED = 0xFFFF


def scale_registers(registers: List[Number]) -> List[float]:
    scale = math.pow(10, registers[-1])
    return [register * scale if register != UINT16_UNSUPPORTED else 0 for register in registers[:-1]]
