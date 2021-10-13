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


class Lovato:
    def __init__(self, device_config: dict, client: connect_tcp.ConnectTcp) -> None:
        self.client = client
        self.name = device_config["components"]["component0"]["name"]
        self.id = device_config["components"]["component0"]["configuration"]["id"]

    def get_voltage(self) -> List[int]:
        """
        """
        try:
            voltage = []
            regs = [0x0001, 0x0003, 0x0005]
            for register in regs:
                value = float(self.client.read_registers(register, 2, self.id) / 100)
                voltage.append(value)
            return voltage
        except Exception as e:
            log.MainLogger().error(self.name, e)
            return [None, None, None]

    def get_imported(self) -> float:
        """
        """
        try:
            imported = self.client.read_float_registers(0x0048, 2, self.id) * 1000
            return imported
        except Exception as e:
            log.MainLogger().error(self.name, e)
            return None

    def get_power(self) -> Tuple[List[int], float]:
        try:
            power_per_phase = []
            regs = [0x0013, 0x0015, 0x0017]
            for register in regs:
                value = self.client.read_integer_registers(register, 2, self.id) / 100
                power_per_phase.append(value)

            if self.type == "Bat-Kit":
                power_all = self.client.read_float_registers(0x000C, 2, self.id)
            else:
                power_all = sum(power_per_phase)

            return power_per_phase, power_all
        except Exception as e:
            log.MainLogger().error(self.name, e)
            return [None, None, None], None

    def get_exported(self) -> float:
        """
        """
        try:
            exported = self.client.read_float_registers(0x004a, 2, self.id) * 1000
            return exported
        except Exception as e:
            log.MainLogger().error(self.name, e)
            return None

    def get_power_factor(self) -> List[int]:
        """
        """
        try:
            power_factor = []
            regs = [0x0025, 0x0027, 0x0029]
            for register in regs:
                value = float(self.client.read_registers(register, 2, self.id)) / 10000
                power_factor.append(value)
            return power_factor
        except Exception as e:
            log.MainLogger().error(self.name, e)
            return [None, None, None]

    def get_frequency(self) -> float:
        """
        """
        try:
            frequency = float(self.client.read_registers(0x0031, 2, self.id)) / 100
            if frequency > 100:
                frequency = frequency / 10
            return frequency
        except Exception as e:
            log.MainLogger().error(self.name, e)
            return None

    def get_current(self) -> List[int]:
        """
        """
        try:
            current = []
            regs = [0x0007, 0x0009, 0x000b]
            for register in regs:
                value = self.client.read_integer_registers(register, 2, self.id) / 10000
                current.append(value)
            return current
        except Exception as e:
            log.MainLogger().error(self.name, e)
            return [None, None, None]

    def get_counter(self) -> float:
        try:
            finalbezug1 = self.client.read_integer_registers(0x1a1f, 2, self.id)
            finalbezug2 = self.client.read_input_registers(0x1a21, 2, self.id)
            if (finalbezug1 > finalbezug2):
                counter = finalbezug1
            else:
                counter = finalbezug2
            return counter
        except Exception as e:
            log.log_exception_comp(e, self.ramdisk, self.type+str(self.pv_num))
            return None
