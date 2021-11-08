#!/usr/bin/env python3
import sys
from typing import List, Tuple

try:
    from ..common import connect_tcp
    from ..common.module_error import ModuleError, ModuleErrorLevels
except:
    # for 1.9 compability
    from pathlib import Path
    import sys
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
    from modules.common import connect_tcp
    from modules.common.module_error import ModuleError, ModuleErrorLevels


class Sdm630:
    def __init__(self, modbus_id: int, client: connect_tcp.ConnectTcp) -> None:
        self.client = client
        self.id = modbus_id

    def __process_error(self, e):
        if isinstance(e, ModuleError):
            raise
        else:
            raise ModuleError(__name__+" "+str(type(e))+" "+str(e), ModuleErrorLevels.ERROR) from e

    def get_voltage(self) -> List[float]:
        try:
            return [self.client.read_float_registers(register, 2, self.id) for register in [0x00, 0x02, 0x04]]
        except Exception as e:
            self.__process_error(e)

    def get_imported(self) -> float:
        try:
            return self.client.read_float_registers(0x0048, 2, self.id) * 1000
        except Exception as e:
            self.__process_error(e)

    def get_power(self) -> Tuple[List[float], float]:
        try:
            power_per_phase = [self.client.read_float_registers(register, 2, self.id) for register in [0x0C, 0x0E, 0x10]]
            power_all = sum(power_per_phase)
            return power_per_phase, power_all
        except Exception as e:
            self.__process_error(e)

    def get_exported(self) -> float:
        try:
            return self.client.read_float_registers(0x004a, 2, self.id) * 1000
        except Exception as e:
            self.__process_error(e)

    def get_power_factor(self) -> List[float]:
        try:
            return [self.client.read_float_registers(register, 2, self.id) for register in [0x1E, 0x20, 0x22]]
        except Exception as e:
            self.__process_error(e)

    def get_frequency(self) -> float:
        try:
            frequency = self.client.read_float_registers(0x46, 2, self.id)
            if frequency > 100:
                frequency = frequency / 10
            return frequency
        except Exception as e:
            self.__process_error(e)

    def get_current(self) -> List[float]:
        try:
            return [self.client.read_float_registers(register, 2, self.id) for register in [0x06, 0x08, 0x0A]]
        except Exception as e:
            self.__process_error(e)

    def get_counter(self) -> float:
        try:
            return self.client.read_float_registers(0x0156, 2, self.id) * 1000
        except Exception as e:
            self.__process_error(e)
