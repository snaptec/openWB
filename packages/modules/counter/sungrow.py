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

            try:
                if self.data["config"]["mode"] == 1:
                    resp = client.read_input_registers(5082, 2, unit=1)
                    value1 = resp.registers[0]
                    value2 = resp.registers[1]
                    all = format(value2, '04x') + format(value1, '04x')
                    power_all = int(struct.unpack('>i', all.decode('hex'))[0])
                else:
                    resp = client.read_input_registers(13009, 2, unit=1)
                    value1 = resp.registers[0]
                    value2 = resp.registers[1]
                    all = format(value2, '04x') + format(value1, '04x')
                    power_all = int(struct.unpack('>i', all.decode('hex'))[0]*-1)
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
        mode = int(sys.argv[2])
        mod.data["config"]["mode"] = mode

        if int(os.environ.get('debug')) >= 2:
            log.log_1_9('Counter-Module sungrow ip_address: ' + str(ip_address))
            log.log_1_9('Counter-Module sungrow mode: ' + str(mode))

        mod.read()
    except Exception as e:
        log.log_exception_comp(e, True)
