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
addext = int(sys.argv[2])

client = ModbusTcpClient(ipaddress, port=502)

# battsoc
resp= client.read_holding_registers(40082,1,unit=1)
value1 = resp.registers[0]
all = format(value1, '04x')
final = int(struct.unpack('>h', all.decode('hex'))[0]) 
f = open('/var/www/html/openWB/ramdisk/speichersoc', 'w')
f.write(str(final))
f.close()
# print "hausverbrauch"
# resp= client.read_holding_registers(40071,2,unit=1)
# value1 = resp.registers[0]
# value2 = resp.registers[1]
# all = format(value2, '04x') + format(value1, '04x')
# final = int(struct.unpack('>i', all.decode('hex'))[0])
# print final
# pv punkt
ext = 0
if addext == 1:
    resp= client.read_holding_registers(40075,2,unit=1)
    value1 = resp.registers[0]
    value2 = resp.registers[1]
    all = format(value2, '04x') + format(value1, '04x')
    ext = int(struct.unpack('>i', all.decode('hex'))[0])
resp= client.read_holding_registers(40067,2,unit=1)
value1 = resp.registers[0]
value2 = resp.registers[1]
all = format(value2, '04x') + format(value1, '04x')
final = int(struct.unpack('>i', all.decode('hex'))[0]) * -1
f = open('/var/www/html/openWB/ramdisk/pvwatt', 'w')
f.write(str(final+ext))
f.close()
#battleistung
resp= client.read_holding_registers(40069,2,unit=1)
value1 = resp.registers[0]
value2 = resp.registers[1]
all = format(value2, '04x') + format(value1, '04x')
final = int(struct.unpack('>i', all.decode('hex'))[0])
f = open('/var/www/html/openWB/ramdisk/speicherleistung', 'w')
f.write(str(final))
f.close()
