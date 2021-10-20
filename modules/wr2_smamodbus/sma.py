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

# pv watt
resp= client.read_holding_registers(30775,2,unit=3)
value1 = resp.registers[0]
value2 = resp.registers[1]
all = format(value1, '04x') + format(value2, '04x')
final = int(struct.unpack('>i', all.decode('hex'))[0])
if final < 0:
    final = 0
final = final * -1
f = open('/var/www/html/openWB/ramdisk/pv2watt', 'w')
f.write(str(final))
f.close()

# pv Wh
resp= client.read_holding_registers(30529,2,unit=3)
value1 = resp.registers[0]
value2 = resp.registers[1]
all = format(value1, '04x') + format(value2, '04x')
final = int(struct.unpack('>i', all.decode('hex'))[0])
f = open('/var/www/html/openWB/ramdisk/pv2kwh', 'w')
f.write(str(final))
f.close()
