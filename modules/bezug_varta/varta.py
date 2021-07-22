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

# gridleistung
resp= client.read_holding_registers(1078,1,unit=1)
value1 = resp.registers[0]
all = format(value1, '04x')
final = int(struct.unpack('>h', all.decode('hex'))[0])*-1 
f = open('/var/www/html/openWB/ramdisk/wattbezug', 'w')
f.write(str(final))
f.close()
