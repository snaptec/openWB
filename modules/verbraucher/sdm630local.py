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

#Phase 1 A
resp = client.read_input_registers(0x06,2, unit=sdmid)
al1 = struct.unpack('>f',struct.pack('>HH',*resp.registers))
al1 = float("%.3f" % al1[0])
al1string = "/var/www/html/openWB/ramdisk/verbraucher%s_a1" % (verbrauchernr)
f = open(al1string, 'w')
f.write(str(al1))
f.close()

#Phase 2 A
resp = client.read_input_registers(0x08,2, unit=sdmid)
al2 = struct.unpack('>f',struct.pack('>HH',*resp.registers))
al2= float("%.3f" % al2[0])
al2string = "/var/www/html/openWB/ramdisk/verbraucher%s_a2" % (verbrauchernr)
f = open(al2string, 'w')
f.write(str(al2))
f.close()

#Phase 3 A
resp = client.read_input_registers(0x0A,2, unit=sdmid)
al3 = struct.unpack('>f',struct.pack('>HH',*resp.registers))
al3 = float("%.3f" % al3[0])
al3string = "/var/www/html/openWB/ramdisk/verbraucher%s_a3" % (verbrauchernr)
f = open(al3string, 'w')
f.write(str(al3))
f.close()

#Phase 1 V
resp = client.read_input_registers(0x00,2, unit=sdmid)
vl1 = struct.unpack('>f',struct.pack('>HH',*resp.registers))
vl1 = float("%.3f" % vl1[0])
vl1string = "/var/www/html/openWB/ramdisk/verbraucher%s_v1" % (verbrauchernr)
f = open(vl1string, 'w')
f.write(str(vl1))
f.close()

#Phase 2 V
resp = client.read_input_registers(0x02,2, unit=sdmid)
vl2 = struct.unpack('>f',struct.pack('>HH',*resp.registers))
vl2 = float("%.3f" % vl2[0])
vl2string = "/var/www/html/openWB/ramdisk/verbraucher%s_v2" % (verbrauchernr)
f = open(vl2string, 'w')
f.write(str(vl2))
f.close()

#Phase 3 V
resp = client.read_input_registers(0x04,2, unit=sdmid)
vl3 = struct.unpack('>f',struct.pack('>HH',*resp.registers))
vl3 = float("%.3f" % vl3[0])
vl3string = "/var/www/html/openWB/ramdisk/verbraucher%s_v3" % (verbrauchernr)
f = open(vl3string, 'w')
f.write(str(vl3))
f.close()
#KWH Total
resp = client.read_input_registers(0x0156,2, unit=sdmid)
vwh = struct.unpack('>f',struct.pack('>HH',*resp.registers))
vwh2 = float("%.3f" % vwh[0]) * int(1000)
vwh3 = str(vwh2)
vwhstring = "/var/www/html/openWB/ramdisk/verbraucher%s_wh" % (verbrauchernr)
f = open(vwhstring, 'w')
f.write(str(vwh3))
f.close()

#KWH Total Export
#L1
resp = client.read_input_registers(0x0160,2, unit=sdmid)
l1whe = struct.unpack('>f',struct.pack('>HH',*resp.registers))
l1whe2 = float("%.3f" % l1whe[0]) * int(1000)
l1whe3 = str(l1whe2)
vwhsel1tring = "/var/www/html/openWB/ramdisk/verbraucher%s_whel1" % (verbrauchernr)
f = open(vwhsel1tring, 'w')
f.write(str(l1whe3))
f.close()

#L2
resp = client.read_input_registers(0x0162,2, unit=sdmid)
l2whe = struct.unpack('>f',struct.pack('>HH',*resp.registers))
l2whe2 = float("%.3f" % l2whe[0]) * int(1000)
l2whe3 = str(l2whe2)
vwhel2string = "/var/www/html/openWB/ramdisk/verbraucher%s_whel2" % (verbrauchernr)
f = open(vwhel2string, 'w')
f.write(str(l2whe3))
f.close()

#L3
resp = client.read_input_registers(0x0164,2, unit=sdmid)
l3whe = struct.unpack('>f',struct.pack('>HH',*resp.registers))
l3whe2 = float("%.3f" % l3whe[0]) * int(1000)
l3whe3 = str(l3whe2)
vwhel3string = "/var/www/html/openWB/ramdisk/verbraucher%s_whel3" % (verbrauchernr)
f = open(vwhel3string, 'w')
f.write(str(l3whe3))
f.close()

#Totoal Export
whe=l1whe2+l2whe2+l3whe2
vwhestring = "/var/www/html/openWB/ramdisk/verbraucher%s_whe" % (verbrauchernr)
f = open(vwhestring, 'w')
f.write(str(whe))
f.close()

#Aktueller Verbrauch
resp = client.read_input_registers(0x0034,2, unit=sdmid)
watt = struct.unpack('>f',struct.pack('>HH',*resp.registers))
watt = int(watt[0])
wattstring = "/var/www/html/openWB/ramdisk/verbraucher%s_watt" % (verbrauchernr)
f = open(wattstring, 'w')
f.write(str(watt))
f.close()
