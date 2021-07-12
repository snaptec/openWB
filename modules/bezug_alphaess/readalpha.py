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
resp = client.read_holding_registers(0x0006,4, unit=sdmid)
decoder = BinaryPayloadDecoder.fromRegisters(resp.registers,byteorder=Endian.Big,wordorder=Endian.Big)
gridw = int(decoder.decode_32bit_int())
f = open('/var/www/html/openWB/ramdisk/wattbezug', 'w')
f.write(str(gridw))
f.close()

resp = client.read_holding_registers(0x0008,4, unit=sdmid)
decoder = BinaryPayloadDecoder.fromRegisters(resp.registers,byteorder=Endian.Big,wordorder=Endian.Big)
einspwh = int(decoder.decode_32bit_int()) * 10
#print('grideinwh'+str(einspwh))
f = open('/var/www/html/openWB/ramdisk/einspeisungkwh', 'w')
f.write(str(einspwh))
f.close()

resp = client.read_holding_registers(0x000A,4, unit=sdmid)
decoder = BinaryPayloadDecoder.fromRegisters(resp.registers,byteorder=Endian.Big,wordorder=Endian.Big)
bezugwh = int(decoder.decode_32bit_int()) * 10
#print('gridbezugwh'+str(bezugwh))
f = open('/var/www/html/openWB/ramdisk/bezugkwh', 'w')
f.write(str(bezugwh))
f.close()

resp = client.read_holding_registers(0x0000,4, unit=sdmid)
decoder = BinaryPayloadDecoder.fromRegisters(resp.registers,byteorder=Endian.Big,wordorder=Endian.Big)
gridw = int(decoder.decode_32bit_int())
final = gridw / 230
f = open('/var/www/html/openWB/ramdisk/bezuga1', 'w')
f.write(str(final))
f.close()

resp = client.read_holding_registers(0x0002,4, unit=sdmid)
decoder = BinaryPayloadDecoder.fromRegisters(resp.registers,byteorder=Endian.Big,wordorder=Endian.Big)
gridw = int(decoder.decode_32bit_int())
final = gridw / 230
f = open('/var/www/html/openWB/ramdisk/bezuga2', 'w')
f.write(str(final))
f.close()

resp = client.read_holding_registers(0x0004,4, unit=sdmid)
decoder = BinaryPayloadDecoder.fromRegisters(resp.registers,byteorder=Endian.Big,wordorder=Endian.Big)
gridw = int(decoder.decode_32bit_int())
final = gridw / 230
f = open('/var/www/html/openWB/ramdisk/bezuga3', 'w')
f.write(str(final))
f.close()
