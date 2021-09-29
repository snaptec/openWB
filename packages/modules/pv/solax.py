#!/usr/bin/env python3
import sys
from pymodbus.client.sync import ModbusTcpClient

if __name__ == "__main__":
    from pathlib import Path
    import os
    parentdir2 = str(Path(os.path.abspath(__file__)).parents[2])
    sys.path.insert(0, parentdir2)
    from helpermodules import log
    from helpermodules import pub
    import set_values
else:
    from ...helpermodules import log
    from ...helpermodules import pub
    from . import set_values


class module(set_values.set_values):
    def __init__(self, pv_num, ramdisk=False) -> None:
        super().__init__()
        self.ramdisk = ramdisk
        self.data = {}
        self.data["simulation"] = {}
        self.pv_num = pv_num

    def _unsigned32(self, result, addr):
        low = result.registers[addr]
        high = result.registers[addr + 1]
        val = low + (high << 16)
        return val

    def _unsigned16(self, result, addr):
        return result.registers[addr]

    def _signed16(self, result, addr):
        val = addr
        if val > 32767:
            val -= 65535
        return val

    def read(self):
        try:
            client = ModbusTcpClient(self.data["config"]["ip_address"], port=502)

            try:
                resp = client.read_input_registers(10, 2)
                pv1 = self._unsigned16(resp, 0)
                pv2 = self._unsigned16(resp, 1)
                power = (pv1 + pv2) * -1
            except Exception as e:
                log.log_exception_comp(e, self.ramdisk, "PV"+str(self.pv_num))
                power = 0

            try:
                resp = client.read_input_registers(80, 4)
                daily_yield = self._unsigned32(resp, 0) / 10   # yield today
            except Exception as e:
                log.log_exception_comp(e, self.ramdisk, "PV"+str(self.pv_num))
                daily_yield = 0
            if self.ramdisk == True:
                with open("/var/www/html/openWB/ramdisk/daily_pvkwh", "w") as f:
                    f.write(str(daily_yield))
            else:
                pub.pub("openWB/set/pv/"+str(self.pv_num)+"/get/daily_yield", round(daily_yield[0], 2))

            try:
                counter = self._unsigned32(resp, 2)       # yield overall
            except Exception as e:
                log.log_exception_comp(e, self.ramdisk, "PV"+str(self.pv_num))
                counter = 0

            client.close()

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
