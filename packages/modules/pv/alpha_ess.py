#!/usr/bin/env python3
import time
from pymodbus.payload import BinaryPayloadDecoder
from pymodbus.constants import Endian
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
    def __init__(self, pv_num, ramdisk=False) -> None:
        super().__init__()
        self.ramdisk = ramdisk
        self.data = {}
        self.data["simulation"] = {}
        self.pv_num = pv_num

    def read(self):
        try:
            if self.data["module"]["config"]["version"] == 0:
                self._read_alpha_prior_v123()
            elif self.data["module"]["config"]["version"] == 1:
                self._read_alpha_since_v123()
        except Exception as e:
            log.log_exception_comp(e, self.ramdisk)

    def _read_alpha_prior_v123(self):
        try:
            client = ModbusTcpClient('192.168.193.125', port=8899)

            try:
                sdmid = int(85)
                resp = client.read_holding_registers(0x0012, 4, unit=sdmid)
                decoder = BinaryPayloadDecoder.fromRegisters(resp.registers, byteorder=Endian.Big, wordorder=Endian.Big)
                pvw = int(decoder.decode_32bit_int())
                if (pvw < 0):
                    pvw = pvw * -1
                time.sleep(0.1)
                resp = client.read_holding_registers(0x041F, 4, unit=sdmid)
                decoder = BinaryPayloadDecoder.fromRegisters(resp.registers, byteorder=Endian.Big, wordorder=Endian.Big)
                pvw2 = int(decoder.decode_32bit_int())
                resp = client.read_holding_registers(0x0423, 4, unit=sdmid)
                decoder = BinaryPayloadDecoder.fromRegisters(resp.registers, byteorder=Endian.Big, wordorder=Endian.Big)
                pvw3 = int(decoder.decode_32bit_int())
                resp = client.read_holding_registers(0x0427, 4, unit=sdmid)
                decoder = BinaryPayloadDecoder.fromRegisters(resp.registers, byteorder=Endian.Big, wordorder=Endian.Big)
                pvw4 = int(decoder.decode_32bit_int())
                power = (pvw + pvw2 + pvw3 + pvw4) * -1
            except Exception as e:
                log.log_exception_comp(e, self.ramdisk)
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
            log.log_exception_comp(e, self.ramdisk)

    def _read_alpha_since_v123(self):
        try:
            client = ModbusTcpClient('192.168.193.125', port=8899)

            try:
                sdmid = int(85)
                resp = client.read_holding_registers(0x00A1, 4, unit=sdmid)
                decoder = BinaryPayloadDecoder.fromRegisters(resp.registers, byteorder=Endian.Big, wordorder=Endian.Big)
                pvw = int(decoder.decode_32bit_int())
                if (pvw < 0):
                    pvw = pvw * -1
                time.sleep(0.1)
                resp = client.read_holding_registers(0x041F, 4, unit=sdmid)
                decoder = BinaryPayloadDecoder.fromRegisters(resp.registers, byteorder=Endian.Big, wordorder=Endian.Big)
                pvw2 = int(decoder.decode_32bit_int())
                resp = client.read_holding_registers(0x0423, 4, unit=sdmid)
                decoder = BinaryPayloadDecoder.fromRegisters(resp.registers, byteorder=Endian.Big, wordorder=Endian.Big)
                pvw3 = int(decoder.decode_32bit_int())
                resp = client.read_holding_registers(0x0427, 4, unit=sdmid)
                decoder = BinaryPayloadDecoder.fromRegisters(resp.registers, byteorder=Endian.Big, wordorder=Endian.Big)
                pvw4 = int(decoder.decode_32bit_int())
                power = (pvw + pvw2 + pvw3 + pvw4) * -1
            except Exception as e:
                log.log_exception_comp(e, self.ramdisk)
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
            log.log_exception_comp(e, self.ramdisk)


if __name__ == "__main__":
    try:
        mod = module(0, True)
        mod.data["module"] = {}
        mod.data["module"]["config"] = {}
        version = int(sys.argv[1])
        mod.data["module"]["config"]["version"] = version

        mod.read()
    except Exception as e:
        log.log_exception_comp(e, True)
