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
slave1id = int(sys.argv[2])
slave2id = int(sys.argv[3])
batwrsame = int(sys.argv[4])
extprodakt = int(sys.argv[5])

client = ModbusTcpClient(ipaddress, port=502)

# batterie auslesen und pv leistung korrigieren
storagepower = 0
if batwrsame == 1:
    rr = client.read_holding_registers(62836, 2, unit=1)
    raw = struct.pack('>HH', rr.getRegister(1), rr.getRegister(0))
    storagepower = int(struct.unpack('>f', raw)[0])

# wr1
resp= client.read_holding_registers(40084,2,unit=slave1id)
multipli = resp.registers[0]
multiplint = format(multipli, '04x')
fmultiplint = int(struct.unpack('>h', multiplint.decode('hex'))[0])

respw= client.read_holding_registers(40083,2,unit=slave1id)
value1w = respw.registers[0]
allw = format(value1w, '04x')
rawprodw = finalw = int(struct.unpack('>h', allw.decode('hex'))[0]) * -1
if fmultiplint == 0:
    rawprodw = rawprodw
if fmultiplint == -1:
    rawprodw = rawprodw / 10 
if fmultiplint == -2:
    rawprodw = rawprodw / 100
if fmultiplint == -3:
    rawprodw = rawprodw / 1000
if fmultiplint == -4:
    rawprodw = rawprodw / 10000

resp= client.read_holding_registers(40093,2,unit=slave1id)
value1 = resp.registers[0]
value2 = resp.registers[1]
all = format(value1, '04x') + format(value2, '04x')
final = int(struct.unpack('>i', all.decode('hex'))[0])

# wr2
resp= client.read_holding_registers(40084,2,unit=slave2id)
multipli = resp.registers[0]
multiplint = format(multipli, '04x')
fmultiplint = int(struct.unpack('>h', multiplint.decode('hex'))[0])

respw= client.read_holding_registers(40083,2,unit=slave2id)
value1w = respw.registers[0]
allw = format(value1w, '04x')
rawprod2w = finalw = int(struct.unpack('>h', allw.decode('hex'))[0]) * -1
if fmultiplint == 0:
    rawprod2w = rawprod2w
if fmultiplint == -1:
    rawprod2w = rawprod2w / 10 
if fmultiplint == -2:
    rawprod2w = rawprod2w / 100
if fmultiplint == -3:
    rawprod2w = rawprod2w / 1000
if fmultiplint == -4:
    rawprod2w = rawprod2w / 10000

if extprodakt == 1:    
    resp= client.read_holding_registers(40380,1,unit=slave1id)
    value1 = resp.registers[0]
    all = format(value1, '04x')
    extprod = int(struct.unpack('>h', all.decode('hex'))[0]) * -1
else:
    extprod = 0
realrawprodw = rawprodw + rawprod2w + extprod - storagepower
f = open('/var/www/html/openWB/ramdisk/pvwatt', 'w')
f.write(str(realrawprodw))
f.close()

resp= client.read_holding_registers(40093,2,unit=slave2id)
value1 = resp.registers[0]
value2 = resp.registers[1]
all = format(value1, '04x') + format(value2, '04x')
final2 = int(struct.unpack('>i', all.decode('hex'))[0])
rfinal = final + final2
f = open('/var/www/html/openWB/ramdisk/pvkwh', 'w')
f.write(str(rfinal))
f.close()
pvkwhk= rfinal / 1000
f = open('/var/www/html/openWB/ramdisk/pvkwhk', 'w')
f.write(str(pvkwhk))
f.close()
