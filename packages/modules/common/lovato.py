#!/usr/bin/env python3

from typing import List, Tuple

try:
    from ..common import connect_tcp
    from ...helpermodules import log
    from ..common.module_error import ModuleError, ModuleErrorLevels
except:
    # for 1.9 compability
    from pathlib import Path
    import sys
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
    from helpermodules import log
    from modules.common import connect_tcp
    from modules.common.module_error import ModuleError, ModuleErrorLevels


class Lovato:
    def __init__(self, modbus_id: int, client: connect_tcp.ConnectTcp) -> None:
        self.client = client
        self.id = modbus_id

    def __process_error(self, e):
        if isinstance(e, ModuleError):
            raise
        else:
            raise ModuleError(__name__+" "+str(type(e))+" "+str(e), ModuleErrorLevels.ERROR) from e

    def get_voltage(self) -> List[int]:
        try:
            return [self.client.read_registers(register, 2, self.id) / 100 for register in [0x0001, 0x0003, 0x0005]]
        except Exception as e:
            self.__process_error(e)

    def get_imported(self) -> float:
        try:
            return self.client.read_float_registers(0x0048, 2, self.id) * 1000
        except Exception as e:
            self.__process_error(e)

    def get_power(self) -> Tuple[List[int], float]:
        try:
            power_per_phase = [self.client.read_integer_registers(register, 2, self.id) / 100 for register in [0x0013, 0x0015, 0x0017]]
            power_all = self.client.read_float_registers(0x000C, 2, self.id)
            return power_per_phase, power_all
        except Exception as e:
            self.__process_error(e)

    def get_exported(self) -> float:
        try:
            return self.client.read_float_registers(0x004a, 2, self.id) * 1000
        except Exception as e:
            self.__process_error(e)

    def get_power_factor(self) -> List[int]:
        try:
            return [self.client.read_registers(register, 2, self.id) / 10000 for register in [0x0025, 0x0027, 0x0029]]
        except Exception as e:
            self.__process_error(e)

    def get_frequency(self) -> float:
        try:
            frequency = self.client.read_registers(0x0031, 2, self.id) / 100
            if frequency > 100:
                frequency = frequency / 10
            return frequency
        except Exception as e:
            self.__process_error(e)

    def get_current(self) -> List[int]:
        try:
            return [self.client.read_integer_registers(register, 2, self.id) / 10000 for register in [0x0007, 0x0009, 0x000b]]
        except Exception as e:
            self.__process_error(e)

    def get_counter(self) -> float:
        try:
            finalbezug1 = self.client.read_integer_registers(0x1a1f, 2, self.id)
            finalbezug2 = self.client.read_integer_registers(0x1a21, 2, self.id)
            return max(finalbezug1, finalbezug2)
        except Exception as e:
            self.__process_error(e)
