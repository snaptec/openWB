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

resp= client.read_input_registers(13022,1,unit=1)
value1 = resp.registers[0]
all = format(value1, '04x')
final = int(struct.unpack('>h', all.decode('hex'))[0] / 10 )
f = open('/var/www/html/openWB/ramdisk/speichersoc', 'w')
f.write(str(final))
f.close()

resp= client.read_input_registers(13000,1,unit=1)
value1 = resp.registers[0]
binary=bin(value1)[2:].zfill(8)

# battwatt
resp= client.read_input_registers(13021,1,unit=1)
value1 = resp.registers[0]
all = format(value1, '04x')
final = int(struct.unpack('>h', all.decode('hex'))[0])
if (binary[5] == "1"):
    final=final*-1
f = open('/var/www/html/openWB/ramdisk/speicherleistung', 'w')
f.write(str(final))
f.close()
