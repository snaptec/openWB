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
    import set_values
else:
    from ...helpermodules import log
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
            id = self.data["config"]["id"]
            client = ModbusTcpClient(self.data["config"]["ip_address"], port=8899)

            try:
                resp = client.read_input_registers(0x0006, 2, unit=id)
                al1 = struct.unpack('>f', struct.pack('>HH', *resp.registers))
                current1 = float(al1[0])
            except Exception as e:
                log.log_exception_comp(e, self.ramdisk, "PV"+str(self.pv_num))
                current1 = 0

            try:
                resp = client.read_input_registers(0x000C, 2, unit=id)
                watt = struct.unpack('>f', struct.pack('>HH', *resp.registers))
                watt = int(watt[0])
            except Exception as e:
                log.log_exception_comp(e, self.ramdisk, "PV"+str(self.pv_num))
                power = 0

            try:
                resp = client.read_input_registers(0x004a, 2, unit=id)
                vwh = struct.unpack('>f', struct.pack('>HH', *resp.registers))
                counter = float(vwh[0]) * 1000 * 1000
            except Exception as e:
                log.log_exception_comp(e, self.ramdisk, "PV"+str(self.pv_num))
                counter = 0

            values = [power,
                      counter,
                      [current1, current1, current1]]
            self.set(self.pv_num, values, self.ramdisk)
        except Exception as e:
            log.log_exception_comp(e, self.ramdisk, "PV"+str(self.pv_num))


if __name__ == "__main__":
    try:
        mod = module(0, True)
        mod.data["config"] = {}
        ip_address = str(sys.argv[1])
        mod.data["config"]["ip_address"] = ip_address
        id = int(sys.argv[2])
        mod.data["config"]["id"] = id

        if int(os.environ.get('debug')) >= 2:
            log.log_1_9('PV-Module sdm120 ip_address: ' + str(ip_address))
            log.log_1_9('PV-Module sdm120 id: ' + str(id))

        mod.read()
    except Exception as e:
        log.log_exception_comp(e, True)
