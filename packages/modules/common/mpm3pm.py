#!/usr/bin/env python3
from typing import List, Tuple
try:
    from ..common import connect_tcp
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


class Mpm3pm:
    def __init__(self, device_config: dict, client: connect_tcp.ConnectTcp) -> None:
        self.client = client
        self.name = device_config["components"]["component0"]["name"]
        self.id = device_config["components"]["component0"]["configuration"]["id"]

    def get_voltage(self) -> List[int]:
        """
        """
        try:
            voltage = []
            regs = [0x08, 0x0A, 0x0C]
            for register in regs:
                value = float(self.client.read_registers(register, 4, self.id) / 10)
                voltage.append(value)
            return voltage
        except Exception as e:
            log.MainLogger().error(self.name, e)
            return [None, None, None]

    def get_imported(self) -> float:
        """
        """
        try:
            imported = self.client.read_integer_registers(0x0002, 4, self.id) * 10
            return imported
        except Exception as e:
            log.MainLogger().error(self.name, e)
            return None

    def get_power(self) -> Tuple[List[int], float]:
        try:
            power_per_phase = []
            regs = [0x14, 0x16, 0x18]
            for register in regs:
                value = self.client.read_integer_registers(register, 2, self.id) / 100
                power_per_phase.append(value)
            power_all = self.client.read_integer_registers(0x26, 2, self.id) / 100
            return power_per_phase, power_all
        except Exception as e:
            log.MainLogger().error(self.name, e)
            return [None, None, None], None

    def get_exported(self) -> float:
        """
        """
        try:
            exported = self.client.read_integer_registers(0x0004, 4, self.id) * 10
            return exported
        except Exception as e:
            log.MainLogger().error(self.name, e)
            return None

    def get_power_factor(self) -> List[int]:
        """
        """
        try:
            power_factor = []
            regs = [0x20, 0x22, 0x24]
            for register in regs:
                value = self.client.read_integer_registers(register, 4, self.id) / 10
                power_factor.append(value)
            return power_factor
        except Exception as e:
            log.MainLogger().error(self.name, e)
            return [None, None, None]

    def get_frequency(self) -> float:
        """
        """
        try:
            frequency = self.client.read_integer_registers(0x2c, 4, self.id) / 100
            return frequency
        except Exception as e:
            log.MainLogger().error(self.name, e)
            return None

    def get_current(self) -> List[int]:
        """
        """
        try:
            current = []
            regs = [0x0E, 0x10, 0x12]
            for register in regs:
                value = float(self.client.read_registers(register, 2, self.id)) / 100
                current.append(value)
            return current
        except Exception as e:
            log.MainLogger().error(self.name, e)
            return [None, None, None]

    def get_counter(self) -> float:
        try:
            counter = self.client.read_integer_registers(0x0004, 4, self.id) * 10
            return counter
        except Exception as e:
            log.MainLogger().error(self.name, e)
            return None
