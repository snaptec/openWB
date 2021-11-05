#!/usr/bin/env python3
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


class Mpm3pm:
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
            return [self.client.read_registers(register, 2, self.id) / 10 for register in [0x08, 0x0A, 0x0C]]
        except Exception as e:
            self.__process_error(e)

    def get_imported(self) -> float:
        try:
            return self.client.read_integer_registers(0x0002, 4, self.id) * 10
        except Exception as e:
            self.__process_error(e)

    def get_power(self) -> Tuple[List[int], float]:
        try:
            power_per_phase = [self.client.read_integer_registers(register, 2, self.id) / 100 for register in [0x14, 0x16, 0x18]]
            power_all = self.client.read_integer_registers(0x26, 2, self.id) / 100
            return power_per_phase, power_all
        except Exception as e:
            self.__process_error(e)

    def get_exported(self) -> float:
        try:
            return self.client.read_integer_registers(0x0004, 4, self.id) * 10
        except Exception as e:
            self.__process_error(e)

    def get_power_factor(self) -> List[int]:
        try:
            return [self.client.read_integer_registers(register, 2, self.id) / 100 for register in [0x20, 0x22, 0x24]]
        except Exception as e:
            self.__process_error(e)

    def get_frequency(self) -> float:
        try:
            return self.client.read_integer_registers(0x2c, 4, self.id) / 100
        except Exception as e:
            self.__process_error(e)

    def get_current(self) -> List[int]:
        try:
            return [self.client.read_registers(register, 2, self.id) / 100 for register in [0x0E, 0x10, 0x12]]
        except Exception as e:
            self.__process_error(e)

    def get_counter(self) -> float:
        try:
            return self.client.read_integer_registers(0x0004, 4, self.id) * 10
        except Exception as e:
            self.__process_error(e)
