#!/usr/bin/python
import sys
# import os
# import time
# import getopt
# import socket
# import ConfigParser
import struct
# import binascii
from pymodbus.client.sync import ModbusTcpClient

ipaddress = str(sys.argv[1])

client = ModbusTcpClient(ipaddress, port=502)

# print "SoC batt"
resp= client.read_holding_registers(30845,2,unit=3)
value1 = resp.registers[0]
value2 = resp.registers[1]
all = format(value1, '04x') + format(value2, '04x')
final = int(struct.unpack('>i', all.decode('hex'))[0])
f = open('/var/www/html/openWB/ramdisk/speichersoc', 'w')
f.write(str(final))
f.close()

# print "be-entladen watt"
resp= client.read_holding_registers(31393,2,unit=3)
value1 = resp.registers[0]
value2 = resp.registers[1]
all = format(value1, '04x') + format(value2, '04x')
ladung = int(struct.unpack('>i', all.decode('hex'))[0])
resp= client.read_holding_registers(31395,2,unit=3)
value1 = resp.registers[0]
value2 = resp.registers[1]
all = format(value1, '04x') + format(value2, '04x')
entladung = int(struct.unpack('>i', all.decode('hex'))[0])
if ladung > 5:
    final=ladung
else:
    final=entladung * -1
f = open('/var/www/html/openWB/ramdisk/speicherleistung', 'w')
f.write(str(final))
f.close()
