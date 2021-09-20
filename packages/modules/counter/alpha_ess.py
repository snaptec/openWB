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
    import set_values
else:
    from ...helpermodules import log
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
            if self.data["module"]["config"]["version"] == 0:
                self._read_alpha_prior_v123()
            elif self.data["module"]["config"]["version"] == 1:
                self._read_alpha_since_v123()
        except Exception as e:
            log.log_exception_comp(e, self.ramdisk)

    def _read_alpha_prior_v123(self):
        try:
            client = ModbusTcpClient('192.168.193.125', port=8899)

            sdmid = int(85)
            time.sleep(0.1)
            try:
                resp = client.read_holding_registers(0x0006, 4, unit=sdmid)
                decoder = BinaryPayloadDecoder.fromRegisters(resp.registers, byteorder=Endian.Big, wordorder=Endian.Big)
                power_all = int(decoder.decode_32bit_int())
            except Exception as e:
                log.log_exception_comp(e, self.ramdisk)
                power_all = 0

            try:
                resp = client.read_holding_registers(0x0008, 4, unit=sdmid)
                decoder = BinaryPayloadDecoder.fromRegisters(resp.registers, byteorder=Endian.Big, wordorder=Endian.Big)
                exported = int(decoder.decode_32bit_int()) * 10
            except Exception as e:
                log.log_exception_comp(e, self.ramdisk)
                exported = 0

            try:
                resp = client.read_holding_registers(0x000A, 4, unit=sdmid)
                decoder = BinaryPayloadDecoder.fromRegisters(resp.registers, byteorder=Endian.Big, wordorder=Endian.Big)
                imported = int(decoder.decode_32bit_int()) * 10
            except Exception as e:
                log.log_exception_comp(e, self.ramdisk)
                imported = 0

            try:
                resp = client.read_holding_registers(0x0000, 4, unit=sdmid)
                decoder = BinaryPayloadDecoder.fromRegisters(resp.registers, byteorder=Endian.Big, wordorder=Endian.Big)
                gridw = int(decoder.decode_32bit_int())
                current1 = gridw / 230
                resp = client.read_holding_registers(0x0002, 4, unit=sdmid)
                decoder = BinaryPayloadDecoder.fromRegisters(resp.registers, byteorder=Endian.Big, wordorder=Endian.Big)
                gridw = int(decoder.decode_32bit_int())
                current2 = gridw / 230
                resp = client.read_holding_registers(0x0004, 4, unit=sdmid)
                decoder = BinaryPayloadDecoder.fromRegisters(resp.registers, byteorder=Endian.Big, wordorder=Endian.Big)
                gridw = int(decoder.decode_32bit_int())
                current3 = gridw / 230
            except Exception as e:
                log.log_exception_comp(e, self.ramdisk)
                current1 = 0
                current2 = 0
                current3 = 0

            values = [[0, 0, 0],
                      [current1, current2, current3],
                      [0, 0, ],
                      [0, 0, ],
                      [imported, exported],
                      power_all,
                      50]
            self.set(self.counter_num, values, self.ramdisk)
        except Exception as e:
            log.log_exception_comp(e, self.ramdisk)

    def _read_alpha_since_v123(self):
        try:
            client = ModbusTcpClient('192.168.193.125', port=8899)

            sdmid = int(85)
            time.sleep(0.1)
            try:
                resp = client.read_holding_registers(0x0021, 4, unit=sdmid)
                decoder = BinaryPayloadDecoder.fromRegisters(resp.registers, byteorder=Endian.Big, wordorder=Endian.Big)
                power_all = int(decoder.decode_32bit_int())
            except Exception as e:
                log.log_exception_comp(e, self.ramdisk)
                power_all = 0

            try:
                resp = client.read_holding_registers(0x0010, 4, unit=sdmid)
                decoder = BinaryPayloadDecoder.fromRegisters(resp.registers, byteorder=Endian.Big, wordorder=Endian.Big)
                exported = int(decoder.decode_32bit_int()) * 10
            except Exception as e:
                log.log_exception_comp(e, self.ramdisk)
                exported = 0

            try:
                resp = client.read_holding_registers(0x0012, 4, unit=sdmid)
                decoder = BinaryPayloadDecoder.fromRegisters(resp.registers, byteorder=Endian.Big, wordorder=Endian.Big)
                imported = int(decoder.decode_32bit_int()) * 10
            except Exception as e:
                log.log_exception_comp(e, self.ramdisk)
                imported = 0

            try:
                resp = client.read_holding_registers(0x0017, 2, unit=sdmid)
                decoder = BinaryPayloadDecoder.fromRegisters(resp.registers, byteorder=Endian.Big, wordorder=Endian.Big)
                current1 = int(decoder.decode_16bit_int()/1000)
                resp = client.read_holding_registers(0x0018, 2, unit=sdmid)
                decoder = BinaryPayloadDecoder.fromRegisters(resp.registers, byteorder=Endian.Big, wordorder=Endian.Big)
                current2 = int(decoder.decode_16bit_int()/1000)
                resp = client.read_holding_registers(0x0019, 2, unit=sdmid)
                decoder = BinaryPayloadDecoder.fromRegisters(resp.registers, byteorder=Endian.Big, wordorder=Endian.Big)
                current3 = int(decoder.decode_16bit_int()/1000)
            except Exception as e:
                log.log_exception_comp(e, self.ramdisk)
                current1 = 0
                current2 = 0
                current3 = 0

            values = [[0, 0, 0],
                      [current1, current2, current3],
                      [0, 0, ],
                      [0, 0, ],
                      [imported, exported],
                      power_all,
                      50]
            self.set(self.counter_num, values, self.ramdisk)
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
