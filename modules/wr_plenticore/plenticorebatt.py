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
#PV Leistung
resp= client.read_holding_registers(100,2,unit=71)
FRegister = BinaryPayloadDecoder.fromRegisters(resp.registers, byteorder=Endian.Big, wordorder=Endian.Little)
pvwatt =int(FRegister.decode_32bit_float())
resp= client.read_holding_registers(582,1,unit=71)
FRegister = BinaryPayloadDecoder.fromRegisters(resp.registers, byteorder=Endian.Big, wordorder=Endian.Little)
battwatt =int(FRegister.decode_16bit_int())
fpvwatt = pvwatt - battwatt
fpvwatt = pvwatt * -1
f = open('/var/www/html/openWB/ramdisk/pvwatt', 'w')
f.write(str(fpvwatt))
f.close()
#pv kwh
resp= client.read_holding_registers(320,2,unit=71)
FRegister = BinaryPayloadDecoder.fromRegisters(resp.registers, byteorder=Endian.Big, wordorder=Endian.Little)
final =int(FRegister.decode_32bit_float())
f = open('/var/www/html/openWB/ramdisk/pvkwh', 'w')
f.write(str(final))
f.close()
pvkwhk= final / 1000
f = open('/var/www/html/openWB/ramdisk/pvkwhk', 'w')
f.write(str(pvkwhk))
f.close()





