#!/usr/bin/env python3
import sys
import struct
from pymodbus.client.sync import ModbusTcpClient

if __name__ == "__main__":
    from pathlib import Path
    import os
    import sys
    parentdir2 = str(Path(os.path.abspath(__file__)).parents[2])
    sys.path.insert(0, parentdir2)
    from helpermodules import log
    import set_values
else:
    from ...helpermodules import log
    from . import set_values


class module(set_values.set_values):
    def __init__(self, bat_num, ramdisk=False) -> None:
        super().__init__()
        self.ramdisk = ramdisk
        self.data = {}
        self.data["simulation"] = {}
        self.bat_num = bat_num

    def read(self):
        try:
            client = ModbusTcpClient(self.data["module"]["config"]["ip_address"], port=502)

            try:
                resp = client.read_holding_registers(30845, 2, unit=3)
                value1 = resp.registers[0]
                value2 = resp.registers[1]
                all = format(value1, '04x') + format(value2, '04x')
                soc = int(struct.unpack('>i', all.decode('hex'))[0])
            except Exception as e:
                log.log_exception_comp(e, self.ramdisk)
                soc = 0

            try:
                resp = client.read_holding_registers(30775, 2, unit=3)
                value1 = resp.registers[0]
                value2 = resp.registers[1]
                all = format(value1, '04x') + format(value2, '04x')
                power = int(struct.unpack('>i', all.decode('hex'))[0]) * -1
            except Exception as e:
                log.log_exception_comp(e, self.ramdisk)
                power = 0

            try:
                resp = client.read_holding_registers(30595, 2, unit=3)
                value1 = resp.registers[0]
                value2 = resp.registers[1]
                all = format(value1, '04x') + format(value2, '04x')
                imported = int(struct.unpack('>i', all.decode('hex'))[0])
            except Exception as e:
                log.log_exception_comp(e, self.ramdisk)
                imported = 0

            try:
                resp = client.read_holding_registers(30597, 2, unit=3)
                value1 = resp.registers[0]
                value2 = resp.registers[1]
                all = format(value1, '04x') + format(value2, '04x')
                exported = int(struct.unpack('>i', all.decode('hex'))[0])
            except Exception as e:
                log.log_exception_comp(e, self.ramdisk)
                exported = 0

            values = [power,
                      soc,
                      [imported, exported]]
            self.set(self.bat_num, values, self.ramdisk)
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
