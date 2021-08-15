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
resp= client.read_input_registers(1056,2,unit=25)
value1 = resp.registers[0]
value2 = resp.registers[1]
all = format(value1, '04x') + format(value2, '04x')
final = int(struct.unpack('>i', all.decode('hex'))[0])/10
f = open('/var/www/html/openWB/ramdisk/speichersoc', 'w')
f.write(str(final))
f.close()

# print "be-entladen watt"
resp= client.read_input_registers(1012,2,unit=25)
value1 = resp.registers[0]
value2 = resp.registers[1]
all = format(value1, '04x') + format(value2, '04x')
ladung = int(struct.unpack('>i', all.decode('hex'))[0]) * -1
f = open('/var/www/html/openWB/ramdisk/speicherleistung', 'w')
f.write(str(ladung))
f.close()
