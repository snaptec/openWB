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

resp= client.read_input_registers(5016,2,unit=1)
value1 = resp.registers[0]
value2 = resp.registers[1]
all = format(value2, '04x') + format(value1, '04x')
final = int(struct.unpack('>i', all.decode('hex'))[0]*-1)
f = open('/var/www/html/openWB/ramdisk/pvwatt', 'w')
f.write(str(final))
f.close()
