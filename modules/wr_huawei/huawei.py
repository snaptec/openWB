#!/usr/bin/python
import sys
# import os
import time
# import getopt
# import socket
# import ConfigParser
import struct
# import binascii
from pymodbus.client.sync import ModbusTcpClient

ipaddress = str(sys.argv[1])
idaddress = int(sys.argv[2])
client = ModbusTcpClient(ipaddress, port=502)
connection = client.connect()
time.sleep(7)
# resp= client.read_holding_registers(32066,1,unit=1)
# value1 = resp.registers[0]
# print(str(value1))
# all = format(value1, '04x') + format(value2, '04x')
# final = int(struct.unpack('>i', all.decode('hex'))[0])*-1
# f = open('/var/www/html/openWB/ramdisk/pvwatt', 'w')
# f.write(str(final))
# f.close()
# print(str(final))


#pv watt
resp= client.read_holding_registers(32080,2,unit=idaddress)
value1 = resp.registers[0]
value2 = resp.registers[1]
all = format(value1, '04x') + format(value2, '04x')
final = int(struct.unpack('>i', all.decode('hex'))[0])*-1
f = open('/var/www/html/openWB/ramdisk/pvwatt', 'w')
f.write(str(final))
f.close()

# wattbezug
try:
    resp= client.read_holding_registers(37113,2,unit=idaddress)
    value1 = resp.registers[0]
    value2 = resp.registers[1]
    all = format(value1, '04x') + format(value2, '04x')
    final = int(struct.unpack('>i', all.decode('hex'))[0])*-1
    f = open('/var/www/html/openWB/ramdisk/huawaibezugwatt', 'w')
    f.write(str(final))
    f.close()
except:
    pass
