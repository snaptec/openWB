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

# evu punkt
resp = client.read_input_registers(40002,2, unit=1)
all = format(resp.registers[0], '04x') + format(resp.registers[1], '04x')
finaleinspeisung = int(struct.unpack('>i', all.decode('hex'))[0])
gridw= finaleinspeisung * -1
f = open('/var/www/html/openWB/ramdisk/pvwatt', 'w')
f.write(str(gridw))
f.close()
