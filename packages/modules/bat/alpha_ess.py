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
    def __init__(self, bat_num, ramdisk=False) -> None:
        super().__init__()
        self.ramdisk = ramdisk
        self.data = {}
        self.data["simulation"] = {}
        self.bat_num = bat_num

    def read(self):
        try:
            if self.data["config"]["version"] == 0:
                self._read_alpha_prior_v123()
            elif self.data["config"]["version"] == 1:
                self._read_alpha_since_v123()
        except Exception as e:
            log.log_exception_comp(e, self.ramdisk, "Bat"+str(self.bat_num))

    def _read_alpha_prior_v123(self):
        try:
            client = ModbusTcpClient('192.168.193.125', port=8899)
            sdmid = int(85)
            try:
                time.sleep(0.1)
                # reg bat volt
                resp = client.read_holding_registers(0x0100, 2, unit=sdmid)
                decoder = BinaryPayloadDecoder.fromRegisters(resp.registers, byteorder=Endian.Big, wordorder=Endian.Big)
                voltr = int(decoder.decode_16bit_int())
                time.sleep(0.1)
                # reg battamp
                resp = client.read_holding_registers(0x0101, 2, unit=sdmid)
                decoder = BinaryPayloadDecoder.fromRegisters(resp.registers, byteorder=Endian.Big, wordorder=Endian.Big)
                battcur = int(decoder.decode_16bit_int())
                volt = voltr
                amp = battcur
                power = float(volt * amp * -1 / 100)
            except Exception as e:
                log.log_exception_comp(e, self.ramdisk, "Bat"+str(self.bat_num))
                power = 0

            try:
                time.sleep(0.1)
                # reg batt soc
                resp = client.read_holding_registers(0x0102, 2, unit=sdmid)
                decoder = BinaryPayloadDecoder.fromRegisters(resp.registers, byteorder=Endian.Big, wordorder=Endian.Big)
                w2 = int(decoder.decode_16bit_int())
                soc = int(w2 * 0.1)
            except Exception as e:
                log.log_exception_comp(e, self.ramdisk, "Bat"+str(self.bat_num))
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
            log.log_exception_comp(e, self.ramdisk, "Bat"+str(self.bat_num))

    def _read_alpha_since_v123(self):
        try:
            client = ModbusTcpClient('192.168.193.125', port=8899)
            sdmid = int(85)

            try:
                time.sleep(0.1)
                # reg bat volt
                resp = client.read_holding_registers(0x0100, 2, unit=sdmid)
                decoder = BinaryPayloadDecoder.fromRegisters(resp.registers, byteorder=Endian.Big, wordorder=Endian.Big)
                voltr = int(decoder.decode_16bit_int())
                time.sleep(0.1)
                # reg battamp
                resp = client.read_holding_registers(0x0101, 2, unit=sdmid)
                decoder = BinaryPayloadDecoder.fromRegisters(resp.registers, byteorder=Endian.Big, wordorder=Endian.Big)
                battcur = int(decoder.decode_16bit_int())
                volt = voltr
                amp = battcur
                power = float(volt * amp * -1 / 100)
            except Exception as e:
                log.log_exception_comp(e, self.ramdisk, "Bat"+str(self.bat_num))
                power = 0

            try:
                time.sleep(0.1)
                # reg batt soc
                resp = client.read_holding_registers(0x0102, 2, unit=sdmid)
                decoder = BinaryPayloadDecoder.fromRegisters(resp.registers, byteorder=Endian.Big, wordorder=Endian.Big)
                w2 = int(decoder.decode_16bit_int())
                soc = int(w2 * 0.1)
            except Exception as e:
                log.log_exception_comp(e, self.ramdisk, "Bat"+str(self.bat_num))
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
            log.log_exception_comp(e, self.ramdisk, "Bat"+str(self.bat_num))


if __name__ == "__main__":
    try:
        mod = module(0, True)
        mod.data["config"] = {}
        version = int(sys.argv[1])
        mod.data["config"]["version"] = version

        mod.read()
    except Exception as e:
        log.log_exception_comp(e, True)
