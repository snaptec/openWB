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
resp = client.read_holding_registers(0x00A1,4, unit=sdmid)
decoder = BinaryPayloadDecoder.fromRegisters(resp.registers,byteorder=Endian.Big,wordorder=Endian.Big)
pvw = int(decoder.decode_32bit_int())
if ( pvw < 0 ):
    pvw=pvw * -1
# print('pvw'+str(pvw))
time.sleep(0.1)

resp = client.read_holding_registers(0x041F,4, unit=sdmid)
decoder = BinaryPayloadDecoder.fromRegisters(resp.registers,byteorder=Endian.Big,wordorder=Endian.Big)
pvw2 = int(decoder.decode_32bit_int())
# print('pvw2 '+str(pvw2))

resp = client.read_holding_registers(0x0423,4, unit=sdmid)
decoder = BinaryPayloadDecoder.fromRegisters(resp.registers,byteorder=Endian.Big,wordorder=Endian.Big)
pvw3 = int(decoder.decode_32bit_int())
# print('pvw3 '+str(pvw3))

resp = client.read_holding_registers(0x0427,4, unit=sdmid)
decoder = BinaryPayloadDecoder.fromRegisters(resp.registers,byteorder=Endian.Big,wordorder=Endian.Big)
pvw4 = int(decoder.decode_32bit_int())
# print('pvw4 '+str(pvw4))

# print('pvw2'+str(pvw2))
pvg= (pvw + pvw2 + pvw3 + pvw4) * -1
#print('pvg'+str(pvg))
f = open('/var/www/html/openWB/ramdisk/pvwatt', 'w')
f.write(str(pvg))
f.close()

