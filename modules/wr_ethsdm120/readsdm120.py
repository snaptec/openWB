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

seradd = str(sys.argv[1])
sdmid = int(sys.argv[2])

client = ModbusTcpClient(seradd, port=8899)

resp = client.read_input_registers(0x0006,2, unit=sdmid)
al1 = struct.unpack('>f',struct.pack('>HH',*resp.registers))
al1 = float("%.3f" % al1[0])
f = open("/var/www/html/openWB/ramdisk/pva1", 'w')
f.write(str(al1))
f.close()

resp = client.read_input_registers(0x000C,2, unit=sdmid)
watt = struct.unpack('>f',struct.pack('>HH',*resp.registers))
watt = int(watt[0])
f = open("/var/www/html/openWB/ramdisk/pvwatt", 'w')
f.write(str(watt))
f.close()

resp = client.read_input_registers(0x004a,2, unit=sdmid)
vwh = struct.unpack('>f',struct.pack('>HH',*resp.registers))
vwh1 = float("%.3f" % vwh[0])
vwhk = str(vwh1)
f = open("/var/www/html/openWB/ramdisk/pvkwhk", 'w')
f.write(str(vwhk))
f.close()

vwh2 = float(vwh1) * int(1000)
vwh3 = str(vwh2)
f = open("/var/www/html/openWB/ramdisk/pvkwh", 'w')
f.write(str(vwh3))
f.close()
