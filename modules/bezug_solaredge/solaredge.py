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

resp= client.read_holding_registers(40193,2,unit=1)
multipli = resp.registers[0]
multiplint = format(multipli, '04x')
fmultiplint = int(struct.unpack('>h', multiplint.decode('hex'))[0])
resp= client.read_holding_registers(40190,1,unit=1)
value1 = resp.registers[0]
all = format(value1, '04x')
finala1 = int(struct.unpack('>h', all.decode('hex'))[0]) * -1
resp= client.read_holding_registers(40191,1,unit=1)
value1 = resp.registers[0]
all = format(value1, '04x')
finala2 = int(struct.unpack('>h', all.decode('hex'))[0]) * -1
resp= client.read_holding_registers(40192,1,unit=1)
value1 = resp.registers[0]
all = format(value1, '04x')
finala3 = int(struct.unpack('>h', all.decode('hex'))[0]) * -1


resp= client.read_holding_registers(40193,2,unit=1)
mult2ipli = resp.registers[0]
mult2iplint = format(mult2ipli, '04x')
fmult2iplint = int(struct.unpack('>h', mult2iplint.decode('hex'))[0])

if fmultiplint == fmult2iplint:
    if fmultiplint == 4:
        finala1 = finala1 * 10000
        finala2 = finala2 * 10000
        finala3 = finala3 * 10000
    if fmultiplint == 3:
        finala1 = finala1 * 1000
        finala2 = finala2 * 1000
        finala3 = finala3 * 1000
    if fmultiplint == 2:
        finala1 = finala1 * 100
        finala2 = finala2 * 100
        finala3 = finala3 * 100
    if fmultiplint == 1:
        finala1 = finala1 * 10
        finala2 = finala2 * 10
        finala3 = finala3 * 10
    if fmultiplint == 0:
        finala1 = finala1
        finala2 = finala2
        finala3 = finala3
    if fmultiplint == -1:
        finala1 = finala1 / 10
        finala2 = finala2 / 10
        finala3 = finala3 / 10
    if fmultiplint == -2:
        finala1 = finala1 / 100
        finala2 = finala2 / 100
        finala3 = finala3 / 100
    if fmultiplint == -3:
        finala1 = finala1 / 1000
        finala2 = finala2 / 1000
        finala3 = finala3 / 1000
    if fmultiplint == -4:
        finala1 = finala1 / 10000
        finala2 = finala2 / 10000
        finala3 = finala3 / 10000
    if fmultiplint == -5:
        finala1 = finala1 / 100000
        finala2 = finala2 / 100000
        finala3 = finala3 / 100000
        
f = open('/var/www/html/openWB/ramdisk/bezuga1', 'w')
f.write(str(finala1))
f.close()
f = open('/var/www/html/openWB/ramdisk/bezuga2', 'w')
f.write(str(finala2))
f.close()
f = open('/var/www/html/openWB/ramdisk/bezuga3', 'w')
f.write(str(finala3))
f.close()




#resp= client.read_holding_registers(40084,2,unit=1)
#multipli = resp.registers[0]
#multiplint = format(multipli, '04x')
#fmultiplint = int(struct.unpack('>h', multiplint.decode('hex'))[0])

#respw= client.read_holding_registers(40083,2,unit=1)
#value1w = respw.registers[0]
#allw = format(value1w, '04x')
#rawprodw = finalw = int(struct.unpack('>h', allw.decode('hex'))[0]) * -1
#if fmultiplint == -1:
#    rawprodw = rawprodw / 10 
#if fmultiplint == -2:
#    rawprodw = rawprodw / 100
#if fmultiplint == -3:
#    rawprodw = rawprodw / 1000
#if fmultiplint == -4:
#    rawprodw = rawprodw / 10000
#f = open('/var/www/html/openWB/ramdisk/pvwatt', 'w')
#f.write(str(rawprodw))
#f.close()

#resp= client.read_holding_registers(40093,2,unit=1)
#value1 = resp.registers[0]
#value2 = resp.registers[1]
#all = format(value1, '04x') + format(value2, '04x')
#final = int(struct.unpack('>i', all.decode('hex'))[0])
#f = open('/var/www/html/openWB/ramdisk/pvkwh', 'w')
#f.write(str(final))
#f.close()
#pvkwhk= final / 1000
#f = open('/var/www/html/openWB/ramdisk/pvkwhk', 'w')
#f.write(str(pvkwhk))
#f.close()


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

