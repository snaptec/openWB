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

# print "evu watt bezug"
resp= client.read_holding_registers(30865,2,unit=3)
value1 = resp.registers[0]
value2 = resp.registers[1]
all = format(value1, '04x') + format(value2, '04x')
bezug = int(struct.unpack('>i', all.decode('hex'))[0])
resp= client.read_holding_registers(30867,2,unit=3)
value1 = resp.registers[0]
value2 = resp.registers[1]
all = format(value1, '04x') + format(value2, '04x')
einsp = int(struct.unpack('>i', all.decode('hex'))[0])
if bezug > 5:
    final=bezug
else:
    final=einsp * -1
f = open('/var/www/html/openWB/ramdisk/wattbezug', 'w')
f.write(str(final))
f.close()
