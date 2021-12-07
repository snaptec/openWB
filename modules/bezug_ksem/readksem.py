#!/usr/bin/python
import sys
# import os
# import time
# import getopt
# import struct
from pymodbus.client.sync import ModbusTcpClient
from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadDecoder

class KSEM:
    def __init__(self, ip):
        self.client = ModbusTcpClient(ip, port="502")
        self.client.connect()

    def ReadUInt32(self,addr):
        data=self.client.read_holding_registers(addr, 2, unit=71)
        UInt32register = BinaryPayloadDecoder.fromRegisters(data.registers, byteorder=Endian.Big, wordorder=Endian.Big)
        result = UInt32register.decode_32bit_uint()
        return(result)

    def ReadInt32(self,addr):
        data=self.client.read_holding_registers(addr, 2, unit=71)
        Int32register = BinaryPayloadDecoder.fromRegisters(data.registers, byteorder=Endian.Big, wordorder=Endian.Big)
        result = Int32register.decode_32bit_int()
        return(result)

    def ReadUInt64(self,addr):
        data=self.client.read_holding_registers(addr,4,unit=71)
        UInt64register = BinaryPayloadDecoder.fromRegisters(data.registers, byteorder=Endian.Big, wordorder=Endian.Big)
        result = UInt64register.decode_64bit_uint()
        return(result)

    def write(self, filename, value):
        # print(filename + ": " + str(value))
        f = open(filename, 'w')
        f.write(str(value))
        f.close
        
    def run(self):
        voltage1 = self.ReadUInt32(62) * 0.001
        self.write('/var/www/html/openWB/ramdisk/evuv1', voltage1)

        voltage2 = self.ReadUInt32(102) * 0.001
        self.write('/var/www/html/openWB/ramdisk/evuv2', voltage2)

        voltage3 = self.ReadUInt32(142) * 0.001
        self.write('/var/www/html/openWB/ramdisk/evuv3', voltage3)

        bezugkwh = self.ReadUInt64(512) * 0.1
        self.write('/var/www/html/openWB/ramdisk/bezugkwh', bezugkwh)

        bezugw1p = self.ReadUInt32(40) * 0.1
        bezugw1m = self.ReadUInt32(42) * 0.1
        bezugw1 = bezugw1p if bezugw1p >= bezugw1m else -bezugw1m
        self.write('/var/www/html/openWB/ramdisk/bezugw1', bezugw1)

        bezugw2p = self.ReadUInt32(80) * 0.1
        bezugw2m = self.ReadUInt32(82) * 0.1
        bezugw2 = bezugw2p if bezugw2p >= bezugw2m else -bezugw2m
        self.write('/var/www/html/openWB/ramdisk/bezugw2', bezugw2)

        bezugw3p = self.ReadUInt32(120) * 0.1
        bezugw3m = self.ReadUInt32(122) * 0.1
        bezugw3 = bezugw3p if bezugw3p >= bezugw3m else -bezugw3m
        self.write('/var/www/html/openWB/ramdisk/bezugw3', bezugw3)

        bezuga1 = self.ReadUInt32(60) * 0.001
        self.write('/var/www/html/openWB/ramdisk/bezuga1', bezuga1)

        bezuga2 = self.ReadUInt32(100) * 0.001
        self.write('/var/www/html/openWB/ramdisk/bezuga2', bezuga2)

        bezuga3 = self.ReadUInt32(140) * 0.001
        self.write('/var/www/html/openWB/ramdisk/bezuga3', bezuga3)

        wattbezugp = self.ReadUInt32(0) * 0.1
        wattbezugm = self.ReadUInt32(2) * 0.1
        wattbezug = wattbezugp if wattbezugp >= wattbezugm else -wattbezugm
        finalwattbezug = int(wattbezug)
        self.write('/var/www/html/openWB/ramdisk/wattbezug', finalwattbezug)

        einspeisungkwh = self.ReadUInt64(516) * 0.1
        self.write('/var/www/html/openWB/ramdisk/einspeisungkwh', einspeisungkwh)

        evuhz = self.ReadUInt32(26) * 0.001
        self.write('/var/www/html/openWB/ramdisk/evuhz', evuhz)

        evupf1 = self.ReadInt32(64) * 0.001
        self.write('/var/www/html/openWB/ramdisk/evupf1', evupf1)

        evupf2 = self.ReadInt32(104) * 0.001
        self.write('/var/www/html/openWB/ramdisk/evupf2', evupf2)

        evupf3 = self.ReadInt32(144) * 0.001
        self.write('/var/www/html/openWB/ramdisk/evupf3', evupf3)

def main(argv=None):
    runner = KSEM(argv[1])
    runner.run()

if __name__ == "__main__":
    main(sys.argv)
