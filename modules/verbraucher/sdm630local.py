#!/usr/bin/python
import sys
import os
import time
import getopt
import socket
import ConfigParser
import struct
import binascii
#Args in var schreiben
verbrauchernr = str(sys.argv[1])
seradd = str(sys.argv[2])
sdmid = int(sys.argv[3])

from pymodbus.client.sync import ModbusSerialClient
client = ModbusSerialClient(method = "rtu", port=seradd, baudrate=9600,
                                stopbits=1, bytesize=8, timeout=1)

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
al1string = "/var/www/html/openWB/ramdisk/verbraucher%s_a2" % (verbrauchernr)
f = open(al1string, 'w')
f.write(str(al2))
f.close()

#Phase 3 A
resp = client.read_input_registers(0x0A,2, unit=sdmid)
al3 = struct.unpack('>f',struct.pack('>HH',*resp.registers))
al3 = float("%.3f" % al3[0])
al1string = "/var/www/html/openWB/ramdisk/verbraucher%s_a3" % (verbrauchernr)
f = open(al1string, 'w')
f.write(str(al3))
f.close()

#Phase 1 V
resp = client.read_input_registers(0x00,2, unit=sdmid)
av1 = struct.unpack('>f',struct.pack('>HH',*resp.registers))
av1 = float("%.3f" % av1[0])
av1string = "/var/www/html/openWB/ramdisk/verbraucher%s_v1" % (verbrauchernr)
f = open(al1string, 'w')
f.write(str(av1))
f.close()

#Phase 2 V
resp = client.read_input_registers(0x02,2, unit=sdmid)
av2 = struct.unpack('>f',struct.pack('>HH',*resp.registers))
av2 = float("%.3f" % av2[0])
al1string = "/var/www/html/openWB/ramdisk/verbraucher%s_v2" % (verbrauchernr)
f = open(al1string, 'w')
f.write(str(av1))
f.close()

#Phase 3 V
resp = client.read_input_registers(0x04,2, unit=sdmid)
av3 = struct.unpack('>f',struct.pack('>HH',*resp.registers))
av3 = float("%.3f" % av3[0])
al1string = "/var/www/html/openWB/ramdisk/verbraucher%s_v3" % (verbrauchernr)
f = open(al1string, 'w')
f.write(str(av3))
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

#Aktueller Verbrauch
resp = client.read_input_registers(0x0034,2, unit=sdmid)
watt = struct.unpack('>f',struct.pack('>HH',*resp.registers))
watt = int(watt[0])
wattstring = "/var/www/html/openWB/ramdisk/verbraucher%s_watt" % (verbrauchernr)
f = open(wattstring, 'w')
f.write(str(watt))
f.close()