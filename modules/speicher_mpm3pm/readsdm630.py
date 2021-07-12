#!/usr/bin/python
# import sys
# import os
# import time
# import getopt
import struct
from pymodbus.client.sync import ModbusTcpClient

client = ModbusTcpClient('192.168.193.15', port=8899)

resp = client.read_input_registers(0x0048,2, unit=117)
vwh = struct.unpack('>f',struct.pack('>HH',*resp.registers))
ikwh = float("%.3f" % vwh[0]) * int(1000)
f = open('/var/www/html/openWB/ramdisk/speicherikwh', 'w')
f.write(str(ikwh))
f.close()

# total watt
resp = client.read_input_registers(0x000C,2, unit=117)
watt = struct.unpack('>f',struct.pack('>HH',*resp.registers))
watt1 = int(watt[0])
resp = client.read_input_registers(0x000E,2, unit=117)
watt = struct.unpack('>f',struct.pack('>HH',*resp.registers))
watt2 = int(watt[0])
resp = client.read_input_registers(0x0010,2, unit=117)
watt = struct.unpack('>f',struct.pack('>HH',*resp.registers))
watt3 = int(watt[0])
final=(watt1+watt2+watt3)*-1
f = open('/var/www/html/openWB/ramdisk/speicherleistung', 'w')
f.write(str(final))
f.close()

# export kwh
resp = client.read_input_registers(0x004a,2, unit=117)
vwhe = struct.unpack('>f',struct.pack('>HH',*resp.registers))
ekwh = float("%.3f" % vwhe[0]) * int(1000)
f = open('/var/www/html/openWB/ramdisk/speicherekwh', 'w')
f.write(str(ekwh))
f.close()
