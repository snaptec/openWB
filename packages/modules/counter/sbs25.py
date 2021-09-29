#!/usr/bin/env python3
import sys
import struct
from pymodbus.client.sync import ModbusTcpClient

if __name__ == "__main__":
    from pathlib import Path
    import os
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
    def __init__(self, counter_num, ramdisk=False) -> None:
        super().__init__()
        self.ramdisk = ramdisk
        self.data = {}
        self.data["simulation"] = {}
        self.counter_num = counter_num

    def read(self):
        try:
            client = ModbusTcpClient(self.data["config"]["ip_address"], port=502)

            # print "evu watt bezug"
            try:
                resp = client.read_holding_registers(30865, 2, unit=3)
                value1 = resp.registers[0]
                value2 = resp.registers[1]
                all = format(value1, '04x') + format(value2, '04x')
                bezug = int(struct.unpack('>i', all.decode('hex'))[0])
                resp = client.read_holding_registers(30867, 2, unit=3)
                value1 = resp.registers[0]
                value2 = resp.registers[1]
                all = format(value1, '04x') + format(value2, '04x')
                einsp = int(struct.unpack('>i', all.decode('hex'))[0])
                if bezug > 5:
                    power_all = bezug
                else:
                    power_all = einsp * -1
            except Exception as e:
                log.log_exception_comp(e, self.ramdisk, "Counter"+str(self.counter_num))
                power_all = 0

            if self.ramdisk == True:
                imported, exported = simcount.sim_count(power_all, ramdisk=True, pref="bezug")
            else:
                imported, exported = simcount.sim_count(power_all, topic="openWB/set/counter/"+str(self.counter_num)+"/", data=self.data["simulation"])
            values = [[0, 0, 0],
                      [0, 0, 0],
                      [0, 0, 0],
                      [0, 0, 0],
                      [imported, exported],
                      power_all,
                      50]
            self.set(self.counter_num, values, self.ramdisk)
        except Exception as e:
            log.log_exception_comp(e, self.ramdisk, "Counter"+str(self.counter_num))


if __name__ == "__main__":
    try:
        mod = module(0, True)
        mod.data["config"] = {}
        ip_address = str(sys.argv[1])
        mod.data["config"]["ip_address"] = ip_address

        mod.read()
    except Exception as e:
        log.log_exception_comp(e, True)
