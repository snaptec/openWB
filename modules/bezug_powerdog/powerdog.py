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

#new
resp = client.read_input_registers(40002,2, unit=1)
all = format(resp.registers[0], '04x') + format(resp.registers[1], '04x')
pvwatt = int(struct.unpack('>i', all.decode('hex'))[0])
resp = client.read_input_registers(40026,2, unit=1)
all = format(resp.registers[0], '04x') + format(resp.registers[1], '04x')
hausverbrauch = int(struct.unpack('>i', all.decode('hex'))[0])
final=hausverbrauch-pvwatt

#evu punkt
#resp = client.read_input_registers(40000,2, unit=1)
#all = format(resp.registers[0], '04x') + format(resp.registers[1], '04x')
#finaleinspeisung = int(struct.unpack('>i', all.decode('hex'))[0])
#gridw= finaleinspeisung

#resp = client.read_input_registers(40024,2, unit=1)
#all = format(resp.registers[0], '04x') + format(resp.registers[1], '04x')
#finaleinspeisung = int(struct.unpack('>i', all.decode('hex'))[0])
#hausw= finaleinspeisung

#if gridw > 10:
#    final=gridw *-1
#else:
#    final=hausw
f = open('/var/www/html/openWB/ramdisk/wattbezug', 'w')
f.write(str(final))
f.close()
