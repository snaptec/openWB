#!/usr/bin/python
import sys
import os
import time
import getopt
import socket
import ConfigParser
import struct
import binascii
seradd = str(sys.argv[1])
from pymodbus.client.sync import ModbusTcpClient
client = ModbusTcpClient(seradd, port=8899)


sdmid = int(sys.argv[2])

resp = client.read_input_registers(0x000C,2, unit=sdmid)
watt = struct.unpack('>f',struct.pack('>HH',*resp.registers))
watt = int(watt[0])
if watt > 0:
        watt=watt*-1
f = open("/var/www/html/openWB/ramdisk/pv2watt", 'w')
f.write(str(watt))
f.close()


resp = client.read_input_registers(0x004a,2, unit=sdmid)
vwh = struct.unpack('>f',struct.pack('>HH',*resp.registers))
vwh1 = float("%.3f" % vwh[0])
resp = client.read_input_registers(0x0048,2, unit=sdmid)
v1wh = struct.unpack('>f',struct.pack('>HH',*resp.registers))
v1wh1 = float("%.3f" % v1wh[0])

if vwh1 > v1wh1:
    finalwh=vwh1
else:
    finalwh=v1wh1
vwh2 = float(finalwh) * int(1000)
vwh3 = str(vwh2)
f = open("/var/www/html/openWB/ramdisk/pv2kwh", 'w')
f.write(str(vwh3))
f.close()


