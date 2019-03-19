#!/usr/bin/python
import sys
import os
import time
import getopt
import socket
import ConfigParser
import struct
import binascii
from pymodbus.payload import BinaryPayloadDecoder
from pymodbus.constants import Endian
ipaddress = str(sys.argv[1])
from pymodbus.client.sync import ModbusTcpClient
client = ModbusTcpClient(ipaddress, port=1502)
#evu A 1-3
resp= client.read_holding_registers(222,2,unit=71)
FRegister = BinaryPayloadDecoder.fromRegisters(resp.registers, byteorder=Endian.Big, wordorder=Endian.Little)
final =round(FRegister.decode_32bit_float(),2)
f = open('/var/www/html/openWB/ramdisk/bezuga1', 'w')
f.write(str(final))
f.close()
resp= client.read_holding_registers(232,2,unit=71)
FRegister = BinaryPayloadDecoder.fromRegisters(resp.registers, byteorder=Endian.Big, wordorder=Endian.Little)
final =round(FRegister.decode_32bit_float(),2)
f = open('/var/www/html/openWB/ramdisk/bezuga2', 'w')
f.write(str(final))
f.close()

resp= client.read_holding_registers(242,2,unit=71)
FRegister = BinaryPayloadDecoder.fromRegisters(resp.registers, byteorder=Endian.Big, wordorder=Endian.Little)
final =round(FRegister.decode_32bit_float(),2)
f = open('/var/www/html/openWB/ramdisk/bezuga3', 'w')
f.write(str(final))
f.close()
#EVU Watt
resp= client.read_holding_registers(252,2,unit=71)
FRegister = BinaryPayloadDecoder.fromRegisters(resp.registers, byteorder=Endian.Big, wordorder=Endian.Little)
final =int(FRegister.decode_32bit_float())
final = final - pvwatt
f = open('/var/www/html/openWB/ramdisk/wattbezug', 'w')
f.write(str(final))
f.close()




