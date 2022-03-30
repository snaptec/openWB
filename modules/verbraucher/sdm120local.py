#!/usr/bin/python
import sys
# import os
# import time
# import getopt
# import socket
# import ConfigParser
import struct
# import binascii
from pymodbus.client.sync import ModbusSerialClient

#Args in var schreiben
verbrauchernr = str(sys.argv[1])
seradd = str(sys.argv[2])
sdmid = int(sys.argv[3])

client = ModbusSerialClient(method = "rtu", port=seradd, baudrate=9600, stopbits=1, bytesize=8, timeout=1)

resp = client.read_input_registers(0x0006,2, unit=sdmid)
al1 = struct.unpack('>f',struct.pack('>HH',*resp.registers))
al1 = float("%.3f" % al1[0])
al1string = "/var/www/html/openWB/ramdisk/verbraucher%s_a1" % (verbrauchernr)
f = open(al1string, 'w')
f.write(str(al1))
f.close()

resp = client.read_input_registers(0x000C,2, unit=sdmid)
watt = struct.unpack('>f',struct.pack('>HH',*resp.registers))
watt = int(watt[0])

wattstring = "/var/www/html/openWB/ramdisk/verbraucher%s_watt" % (verbrauchernr)
f = open(wattstring, 'w')
f.write(str(watt))
f.close()

resp = client.read_input_registers(0x0048,2, unit=sdmid)
vwh = struct.unpack('>f',struct.pack('>HH',*resp.registers))
vwh2 = float("%.3f" % vwh[0]) * int(1000)
vwh3 = str(vwh2)
vwhstring = "/var/www/html/openWB/ramdisk/verbraucher%s_wh" % (verbrauchernr)
f = open(vwhstring, 'w')
f.write(str(vwh3))
f.close()

resp = client.read_input_registers(0x004a,2, unit=sdmid)
vwhe = struct.unpack('>f',struct.pack('>HH',*resp.registers))
vwhe2 = float("%.3f" % vwhe[0]) * int(1000)
vwhe3 = str(vwhe2)

vwhestring = "/var/www/html/openWB/ramdisk/verbraucher%s_whe" % (verbrauchernr)
f = open(vwhestring, 'w')
f.write(str(vwhe3))
f.close()
