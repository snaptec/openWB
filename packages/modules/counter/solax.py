#!/usr/bin/env python3
import sys
from pymodbus.client.sync import ModbusTcpClient

if __name__ == "__main__":
    from pathlib import Path
    import os
    parentdir2 = str(Path(os.path.abspath(__file__)).parents[2])
    sys.path.insert(0, parentdir2)
    from helpermodules import log
    import set_values
else:
    from ...helpermodules import log
    from . import set_values


class module(set_values.set_values):
    def __init__(self, counter_num, ramdisk=False) -> None:
        super().__init__()
        self.ramdisk = ramdisk
        self.data = {}
        self.data["simulation"] = {}
        self.counter_num = counter_num

    def _unsigned32(self, result, addr):
        low = result.registers[addr]
        high = result.registers[addr + 1]
        val = low + (high << 16)
        return val

    def _unsigned16(self, result, addr):
        return result.registers[addr]

    def _signed16(self, result, addr):
        val = result.registers[addr]
        if val > 32767:
            val -= 65535
        return val

    def _signed32(self, result, addr):
        val = self._unsigned32(result, addr)
        if val > 2147483647:
            val -= 4294967295
        return val

    def read(self):
        try:
            client = ModbusTcpClient(self.data["module"]["config"]["ip_address"], port=502)

            resp = client.read_input_registers(0, 114)
            try:
                power_all = self._signed32(resp, 70)
                # for SolaX negative means get power from grid
                power_all = -power_all
            except Exception as e:
                log.log_exception_comp(e, self.ramdisk)
                power_all = 0

            try:
                frequency = self._unsigned16(resp, 7) / 100
            except Exception as e:
                log.log_exception_comp(e, self.ramdisk)
                frequency = 0

            try:
                imported = self._unsigned32(resp, 74) / 100
            except Exception as e:
                log.log_exception_comp(e, self.ramdisk)
                imported = 0

            try:
                exported = self._unsigned32(resp, 72) / 100
            except Exception as e:
                log.log_exception_comp(e, self.ramdisk)
                exported = 0

            values = [[0, 0, 0],
                      [0, 0, 0],
                      [0, 0, 0],
                      [0, 0, 0],
                      [imported, exported],
                      power_all,
                      frequency]
            self.set(self.counter_num, values, self.ramdisk)
        except Exception as e:
            log.log_exception_comp(e, self.ramdisk)


if __name__ == "__main__":
    try:
        mod = module(0, True)
        mod.data["module"] = {}
        mod.data["module"]["config"] = {}
        ip_address = str(sys.argv[1])
        mod.data["module"]["config"]["ip_address"] = ip_address

        mod.read()
    except Exception as e:
        log.log_exception_comp(e, True)
