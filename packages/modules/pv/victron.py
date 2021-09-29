#!/usr/bin/env python3
import sys
from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadDecoder
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
            connection = client.connect()

            try:
                resp = client.read_holding_registers(811, 1, unit=100)
                decoder = BinaryPayloadDecoder.fromRegisters(resp.registers, byteorder=Endian.Big, wordorder=Endian.Big)
                mpp1_watt1 = str(decoder.decode_16bit_uint())
                mpp1_watt2 = int(mpp1_watt1)
                resp = client.read_holding_registers(812, 1, unit=100)
                decoder = BinaryPayloadDecoder.fromRegisters(resp.registers, byteorder=Endian.Big, wordorder=Endian.Big)
                mpp2_watt1 = str(decoder.decode_16bit_uint())
                mpp2_watt2 = int(mpp2_watt1)
                resp = client.read_holding_registers(813, 1, unit=100)
                decoder = BinaryPayloadDecoder.fromRegisters(resp.registers, byteorder=Endian.Big, wordorder=Endian.Big)
                mpp3_watt1 = str(decoder.decode_16bit_uint())
                mpp3_watt2 = int(mpp3_watt1)
                # mppt watt
                resp = client.read_holding_registers(850, 1, unit=100)
                decoder = BinaryPayloadDecoder.fromRegisters(resp.registers, byteorder=Endian.Big, wordorder=Endian.Big)
                mpp_watt1 = str(decoder.decode_16bit_uint())
                mpp_watt2 = int(mpp_watt1)

                power = (mpp1_watt2 + mpp2_watt2 + mpp3_watt2 + mpp_watt2) * -1
            except Exception as e:
                log.log_exception_comp(e, self.ramdisk, "PV"+str(self.pv_num))
                power = 0

            client.close()
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
