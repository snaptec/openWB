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
            client = ModbusTcpClient(self.data["config"]["ip_address"], port=502)

            try:
                resp= client.read_input_registers(13022,1,unit=1)
                value1 = resp.registers[0]
                all = format(value1, '04x')
                soc = int(struct.unpack('>h', all.decode('hex'))[0] / 10 )
            except Exception as e:
                log.log_exception_comp(e, self.ramdisk, "Bat"+str(self.bat_num))
                soc = 0

            try:
                resp= client.read_input_registers(13000,1,unit=1)
                value1 = resp.registers[0]
                binary=bin(value1)[2:].zfill(8)
            except Exception as e:
                log.log_exception_comp(e, self.ramdisk, "Bat"+str(self.bat_num))

            # battwatt
            try:
                resp= client.read_input_registers(13021,1,unit=1)
                value1 = resp.registers[0]
                all = format(value1, '04x')
                power = int(struct.unpack('>h', all.decode('hex'))[0])
                if (binary[5] == "1"):
                    power=power*-1
            except Exception as e:
                log.log_exception_comp(e, self.ramdisk, "Bat"+str(self.bat_num))
                power = 0

            if self.ramdisk == True:
                imported, exported = simcount.sim_count(power, ramdisk=True, pref="speicher")
            else:
                imported, exported = simcount.sim_count(power, topic="openWB/set/bat/"+str(self.bat_num)+"/", data=self.data["simulation"])
            values = [power,
                      soc,
                      [imported, exported]]
            self.set(self.bat_num, values, self.ramdisk)
        except Exception as e:
            log.log_exception_comp(e, self.ramdisk, "Bat"+str(self.bat_num))


if __name__ == "__main__":
    try:
        mod = module(0, True)
        mod.data["config"] = {}
        ip_address = str(sys.argv[1])
        mod.data["config"]["ip_address"] = ip_address

        mod.read()
    except Exception as e:
        log.log_exception_comp(e, True)
