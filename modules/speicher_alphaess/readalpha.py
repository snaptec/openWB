#!/usr/bin/python
# import sys
# import os
import time
# import getopt
# import socket
# import ConfigParser
# import struct
# import binascii
# import logging
from pymodbus.payload import BinaryPayloadDecoder
from pymodbus.constants import Endian
from pymodbus.client.sync import ModbusTcpClient

client = ModbusTcpClient('192.168.193.125', port=8899)

sdmid = int(85)
time.sleep(0.1)
# reg bat volt
resp = client.read_holding_registers(0x0100,2, unit=sdmid)
decoder = BinaryPayloadDecoder.fromRegisters(resp.registers,byteorder=Endian.Big,wordorder=Endian.Big)
voltr = int(decoder.decode_16bit_int())
# voltr = resp.registers[0]
# print('volt'+str(voltr))
time.sleep(0.1)
# reg battamp
resp = client.read_holding_registers(0x0101,2, unit=sdmid)
decoder = BinaryPayloadDecoder.fromRegisters(resp.registers,byteorder=Endian.Big,wordorder=Endian.Big)
battcur = int(decoder.decode_16bit_int())
# print('battcur'+str(battcur))
volt = voltr
amp = battcur
# print(volt)
# print(amp)
# print(amp)
battwatt = float(volt * amp * -1 / 100)
battwatt = int(battwatt)
# print(battwatt)
f = open('/var/www/html/openWB/ramdisk/speicherleistung', 'w')
f.write(str(battwatt))
f.close()
time.sleep(0.1)
# reg batt soc
resp = client.read_holding_registers(0x0102,2, unit=sdmid)
decoder = BinaryPayloadDecoder.fromRegisters(resp.registers,byteorder=Endian.Big,wordorder=Endian.Big)
w2 = int(decoder.decode_16bit_int())
socf = int(w2 * 0.1)
# print('battsoc'+str(socf))
f = open('/var/www/html/openWB/ramdisk/speichersoc', 'w')
f.write(str(socf))
f.close()
