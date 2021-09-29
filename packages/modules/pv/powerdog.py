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
    def __init__(self, pv_num, ramdisk=False) -> None:
        super().__init__()
        self.ramdisk = ramdisk
        self.data = {}
        self.data["simulation"] = {}
        self.pv_num = pv_num

    def read(self):
        try:
            client = ModbusTcpClient(self.data["config"]["ip_address"], port=502)

            # evu punkt
            try:
                resp = client.read_input_registers(40002, 2, unit=1)
                all = format(resp.registers[0], '04x') + format(resp.registers[1], '04x')
                finaleinspeisung = int(struct.unpack('>i', all.decode('hex'))[0])
                power = finaleinspeisung * -1
            except Exception as e:
                log.log_exception_comp(e, self.ramdisk, "PV"+str(self.pv_num))
                power = 0

            if self.ramdisk == True:
                _, counter = simcount.sim_count(power, ramdisk=True, pref="pv")
            else:
                _, counter = simcount.sim_count(power, topic="openWB/set/pv/"+str(self.pv_num)+"/", data=self.data["simulation"])
            values = [power,
                      counter,
                      [0, 0, 0]]
            self.set(self.pv_num, values, self.ramdisk)
        except Exception as e:
            log.log_exception_comp(e, self.ramdisk, "PV"+str(self.pv_num))


if __name__ == "__main__":
    try:
        mod = module(0, True)
        mod.data["config"] = {}
        ip_address = str(sys.argv[1])
        mod.data["config"]["ip_address"] = ip_address

        mod.read()
    except Exception as e:
        log.log_exception_comp(e, True)
