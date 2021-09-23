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
    from helpermodules import simcount
    import set_values
else:
    from ...helpermodules import log
    from ...helpermodules import simcount
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
            storage2power = 0
            client = ModbusTcpClient(self.data["module"]["config"]["ip_address"], port=502)

            try:
                rr = client.read_holding_registers(62836, 2, unit=1)
                raw = struct.pack('>HH', rr.getRegister(1), rr.getRegister(0))
                storagepower = int(struct.unpack('>f', raw)[0])
                if self.data["module"]["config"]["second_bat"] == 1:
                    rr = client.read_holding_registers(62836, 2, unit=2)
                    raw = struct.pack('>HH', rr.getRegister(1), rr.getRegister(0))
                    storage2power = int(struct.unpack('>f', raw)[0])
                power = storagepower+storage2power
            except Exception as e:
                log.log_exception_comp(e, self.ramdisk)
                power = 0

            try:
                rr = client.read_holding_registers(62852, 2, unit=1)
                raw = struct.pack('>HH', rr.getRegister(1), rr.getRegister(0))
                soc = int(struct.unpack('>f', raw)[0])
                if self.data["module"]["config"]["second_bat"] == 1:
                    rr = client.read_holding_registers(62852, 2, unit=2)
                    raw = struct.pack('>HH', rr.getRegister(1), rr.getRegister(0))
                    soc2 = int(struct.unpack('>f', raw)[0])
                    soc = (soc+soc2)/2
            except Exception as e:
                log.log_exception_comp(e, self.ramdisk)
                soc = 0

            if self.ramdisk == True:
                imported, exported = simcount.sim_count(power, ramdisk=True, pref="speicher")
            else:
                imported, exported = simcount.sim_count(power, topic="openWB/set/bat/"+str(self.bat_num)+"/", data=self.data["simulation"])
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
        second_bat = int(sys.argv[2])
        mod.data["module"]["config"]["second_bat"] = second_bat

        mod.read()
    except Exception as e:
        log.log_exception_comp(e, True)
