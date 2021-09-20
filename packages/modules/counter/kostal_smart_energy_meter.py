#!/usr/bin/env python3
import sys
from pymodbus.client.sync import ModbusTcpClient
from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadDecoder

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

    def _ReadUInt32(self, addr):
        data = self.client.read_holding_registers(addr, 2, unit=71)
        UInt32register = BinaryPayloadDecoder.fromRegisters(data.registers, byteorder=Endian.Big, wordorder=Endian.Big)
        result = UInt32register.decode_32bit_uint()
        return(result)

    def _ReadInt32(self, addr):
        data = self.client.read_holding_registers(addr, 2, unit=71)
        Int32register = BinaryPayloadDecoder.fromRegisters(data.registers, byteorder=Endian.Big, wordorder=Endian.Big)
        result = Int32register.decode_32bit_int()
        return(result)

    def _ReadUInt64(self, addr):
        data = self.client.read_holding_registers(addr, 4, unit=71)
        UInt64register = BinaryPayloadDecoder.fromRegisters(data.registers, byteorder=Endian.Big, wordorder=Endian.Big)
        result = UInt64register.decode_64bit_uint()
        return(result)

    def read(self):
        try:
            self.client = ModbusTcpClient(self.data["module"]["config"]["ip_address"], port="502")
            self.client.connect()

            try:
                voltage1 = self._ReadUInt32(62) * 0.001
                voltage2 = self._ReadUInt32(102) * 0.001
                voltage3 = self._ReadUInt32(142) * 0.001
            except Exception as e:
                log.log_exception_comp(e, self.ramdisk)
                voltage1 = 0
                voltage2 = 0
                voltage3 = 0

            try:
                imported = self._ReadUInt64(512) * 0.1
            except Exception as e:
                log.log_exception_comp(e, self.ramdisk)
                imported = 0

            try:
                bezugw1p = self._ReadUInt32(40) * 0.1
                bezugw1m = self._ReadUInt32(42) * 0.1
                power1 = bezugw1p if bezugw1p >= bezugw1m else -bezugw1m
                bezugw2p = self._ReadUInt32(80) * 0.1
                bezugw2m = self._ReadUInt32(82) * 0.1
                power2 = bezugw2p if bezugw2p >= bezugw2m else -bezugw2m
                bezugw3p = self._ReadUInt32(120) * 0.1
                bezugw3m = self._ReadUInt32(122) * 0.1
                power3 = bezugw3p if bezugw3p >= bezugw3m else -bezugw3m
            except Exception as e:
                log.log_exception_comp(e, self.ramdisk)
                power1 = 0
                power2 = 0
                power3 = 0

            try:
                current1 = self._ReadUInt32(60) * 0.001
                current2 = self._ReadUInt32(100) * 0.001
                current3 = self._ReadUInt32(140) * 0.001
            except Exception as e:
                log.log_exception_comp(e, self.ramdisk)
                current1 = 0
                current2 = 0
                current3 = 0

            try:
                wattbezugp = self._ReadUInt32(0) * 0.1
                wattbezugm = self._ReadUInt32(2) * 0.1
                wattbezug = wattbezugp if wattbezugp >= wattbezugm else -wattbezugm
                power_all = int(wattbezug)
            except Exception as e:
                log.log_exception_comp(e, self.ramdisk)
                power_all = 0

            try:
                exported = self._ReadUInt64(516) * 0.1
            except Exception as e:
                log.log_exception_comp(e, self.ramdisk)
                exported = 0

            try:
                frequency = self._ReadUInt32(26) * 0.001
            except Exception as e:
                log.log_exception_comp(e, self.ramdisk)
                frequency = 0

            try:
                power_factor1 = self._ReadInt32(64) * 0.001
                power_factor2 = self._ReadInt32(104) * 0.001
                power_factor3 = self._ReadInt32(144) * 0.001
            except Exception as e:
                log.log_exception_comp(e, self.ramdisk)
                power_factor1 = 0
                power_factor2 = 0
                power_factor3 = 0

            values = [[voltage1, voltage2, voltage3],
                      [current1, current2, current3],
                      [power1, power2, power3],
                      [power_factor1, power_factor2, power_factor3],
                      [imported, exported],
                      power_all,
                      frequency]
            self.set(self.counter_num, values, self.ramdisk)
        except Exception as e:
            log.log_exception_comp(e, self.ramdisk)


if __name__ == "__main__":
    try:
        mod = module(0, True)
        mod.data["module"] = {}
        mod.data["module"]["config"] = {}
        ip_address = str(sys.argv[1])
        mod.data["module"]["config"]["ip_address"] = ip_address

        mod.read()
    except Exception as e:
        log.log_exception_comp(e, True)
