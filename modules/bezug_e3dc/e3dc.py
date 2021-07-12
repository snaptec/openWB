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
resp= client.read_holding_registers(40073,2,unit=1)
value1 = resp.registers[0]
value2 = resp.registers[1]
all = format(value2, '04x') + format(value1, '04x')
final = int(struct.unpack('>i', all.decode('hex'))[0])
f = open('/var/www/html/openWB/ramdisk/wattbezug', 'w')
f.write(str(final))
f.close()

volt=230
resp= client.read_holding_registers(40128,4,unit=1)

# print >>f1,(resp.registers)

value1 = resp.registers[0]
all = format(value1, '04x')
finale0 = int(struct.unpack('>h', all.decode('hex'))[0]) 
value1 = resp.registers[1]
all = format(value1, '04x')
finale1 = int(struct.unpack('>h', all.decode('hex'))[0]) 
value1 = resp.registers[2]
all = format(value1, '04x')
finale2 = int(struct.unpack('>h', all.decode('hex'))[0]) 
value1 = resp.registers[3]
all = format(value1, '04x')
finale3 = int(struct.unpack('>h', all.decode('hex'))[0]) 

if finale0 == 1:
    # f1 = open('/var/www/html/openWB/ramdisk/logtest2', 'a')
    # print >>f1,('e3dc zaehler %1d l1 %6d l2 %6d  l3 %6d Watt' % (finale0,finale1,finale2,finale3))
    if finale1 > 0:
        finala1=finale1/volt
    else:
        finala1 = 0
    if finale2 > 0:
        finala2=finale2/volt
    else:
        finala2 = 0
    if finale3 > 0:
        finala3=finale3/volt
    else:
        finala3 = 0
    # print >>f1,('e3dc zaehler %1d l1 %6d l2 %6d  l3 %6d Amp' %  (finale0,finala1,finala2,finala3))
    # volt
    f = open('/var/www/html/openWB/ramdisk/evuv1', 'w')
    f.write(str(volt))
    f.close()
    f = open('/var/www/html/openWB/ramdisk/evuv2', 'w')
    f.write(str(volt))
    f.close()
    f = open('/var/www/html/openWB/ramdisk/evuv3', 'w')
    f.write(str(volt))
    f.close()
    # watt pro phase  
    f = open('/var/www/html/openWB/ramdisk/bezugw1', 'w')
    f.write(str(finale1))
    f.close()
    f = open('/var/www/html/openWB/ramdisk/bezugw2', 'w')
    f.write(str(finale2))
    f.close()
    f = open('/var/www/html/openWB/ramdisk/bezugw3', 'w')
    f.write(str(finale3))
    f.close()
    # amp pro phase
    f = open('/var/www/html/openWB/ramdisk/bezuga1', 'w')
    f.write(str(finala1))
    f.close()
    f = open('/var/www/html/openWB/ramdisk/bezuga2', 'w')
    f.write(str(finala2))
    f.close()
    f = open('/var/www/html/openWB/ramdisk/bezuga3', 'w')
    f.write(str(finala3))
    f.close()
    # f1.close()
