#!/usr/bin/env python3
import sys
from typing import List, Tuple

try:
    from ..common import connect_tcp
    from ..common.module_error import ModuleError
    from ...helpermodules import log
except:
    # for 1.9 compability
    import os
    from pathlib import Path
    import sys
    parentdir2 = str(Path(os.path.abspath(__file__)).parents[2])
    sys.path.insert(0, parentdir2)
    from helpermodules import log
    from modules.common import connect_tcp
    from modules.common.module_error import ModuleError


class Sdm630:
    def __init__(self, component_config: dict, client: connect_tcp.ConnectTcp) -> None:
        self.client = client
        self.name = component_config["name"]
        self.id = component_config["configuration"]["id"]

    def __process_error(self, e):
        if isinstance(e, ModuleError):
            raise
        else:
            raise ModuleError(__name__+" "+str(type(e))+" "+str(e), 2) from e

    def get_voltage(self) -> List[int]:
        try:
            voltage = []
            regs = [0x00, 0x02, 0x04]
            for register in regs:
                value = self.client.read_float_registers(register, 2, self.id)
                voltage.append(value)
            return voltage
        except Exception as e:
            self.__process_error(e)

    def get_imported(self) -> float:
        try:
            return self.client.read_float_registers(0x0048, 2, self.id) * 1000
        except Exception as e:
            self.__process_error(e)

    def get_power(self) -> Tuple[List[int], float]:
        try:
            power_per_phase = []
            regs = [0x0C, 0x0E, 0x10]
            for register in regs:
                value = self.client.read_float_registers(register, 2, self.id)
                power_per_phase.append(value)
            power_all = sum(power_per_phase)
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
            power_factor = []
            regs = [0x1E, 0x20, 0x22]
            for register in regs:
                value = self.client.read_float_registers(register, 2, self.id)
                power_factor.append(value)
            return power_factor
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

    def get_current(self) -> List[int]:
        try:
            current = []
            regs = [0x06, 0x08, 0x0A]
            for register in regs:
                value = self.client.read_float_registers(register, 2, self.id)
                current.append(value)
            return current
        except Exception as e:
            self.__process_error(e)

    def get_counter(self) -> float:
        try:
            return self.client.read_float_registers(0x0156, 2, self.id) * 1000
        except Exception as e:
            self.__process_error(e)
