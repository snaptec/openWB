#!/usr/bin/python
import sys
import os
import time
import getopt
import socket
import ConfigParser
import struct
import binascii
ipaddress = str(sys.argv[1])
from pymodbus.client.sync import ModbusTcpClient
client = ModbusTcpClient(ipaddress, port=502)


resp= client.read_holding_registers(40206,1,unit=1)
value1 = resp.registers[0]
all = format(value1, '04x')
final = int(struct.unpack('>h', all.decode('hex'))[0]) * -1
f = open('/var/www/html/openWB/ramdisk/wattbezug', 'w')
f.write(str(final))
f.close()

resp= client.read_holding_registers(40084,2,unit=1)
multipli = resp.registers[0]
multiplint = format(multipli, '04x')
fmultiplint = int(struct.unpack('>h', multiplint.decode('hex'))[0])

resp= client.read_holding_registers(40083,2,unit=1)
value1 = resp.registers[0]
all = format(value1, '04x')
if fmultiplint == -1:
    final = int(struct.unpack('>h', all.decode('hex'))[0]) / 10 * -1
if fmultiplint == -2:
    final = int(struct.unpack('>h', all.decode('hex'))[0]) / 100 * -1

f = open('/var/www/html/openWB/ramdisk/pvwatt', 'w')
f.write(str(final))
f.close()

resp= client.read_holding_registers(40093,2,unit=1)
value1 = resp.registers[0]
value2 = resp.registers[1]
all = format(value1, '04x') + format(value2, '04x')
final = int(struct.unpack('>i', all.decode('hex'))[0])
f = open('/var/www/html/openWB/ramdisk/pvkwh', 'w')
f.write(str(final))
f.close()
pvkwhk= final / 1000
f = open('/var/www/html/openWB/ramdisk/pvkwhk', 'w')
f.write(str(pvkwhk))
f.close()


resp= client.read_holding_registers(40234,2,unit=1)
value1 = resp.registers[0] 
value2 = resp.registers[1] 
all = format(value1, '04x') + format(value2, '04x')
final = int(struct.unpack('>i', all.decode('hex'))[0]) 
f = open('/var/www/html/openWB/ramdisk/bezugkwh', 'w')
f.write(str(final))
f.close()

resp= client.read_holding_registers(40226,2,unit=1)
value1 = resp.registers[0]
value2 = resp.registers[1] 
all = format(value1, '04x') + format(value2, '04x')
final = int(struct.unpack('>i', all.decode('hex'))[0])
f = open('/var/www/html/openWB/ramdisk/einspeisungkwh', 'w')
f.write(str(final))
f.close()

