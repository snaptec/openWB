#!/usr/bin/python
# import sys
# import os
# import time
# import getopt
import struct
from pymodbus.client.sync import ModbusTcpClient

client = ModbusTcpClient('192.168.193.15', port=8899)
sdmid = 116

# phasen watt
resp = client.read_input_registers(0x0C,2, unit=sdmid)
llw1 = struct.unpack('>f',struct.pack('>HH',*resp.registers))[0]
finalw1 = int(llw1)
resp = client.read_input_registers(0x0E,2, unit=sdmid)
llw1 = struct.unpack('>f',struct.pack('>HH',*resp.registers))[0]
finalw2 = int(llw1)
resp = client.read_input_registers(0x10,2, unit=sdmid)
llw1 = struct.unpack('>f',struct.pack('>HH',*resp.registers))[0]
finalw3 = int(llw1)

finalw= finalw1 + finalw2 + finalw3
if ( finalw > 10):
    finalw=finalw*-1

f = open('/var/www/html/openWB/ramdisk/pvwatt', 'w')
f.write(str(finalw))
f.close()

# ampere l1
resp = client.read_input_registers(0x06,2, unit=sdmid)
lla1 = float(struct.unpack('>f',struct.pack('>HH',*resp.registers))[0])
lla1 = float("%.1f" % lla1)
f = open('/var/www/html/openWB/ramdisk/pva1', 'w')
f.write(str(lla1))
f.close()

# ampere l2
resp = client.read_input_registers(0x08,2, unit=sdmid)
lla1 = float(struct.unpack('>f',struct.pack('>HH',*resp.registers))[0])
lla2 = float("%.1f" % lla1)
f = open('/var/www/html/openWB/ramdisk/pva2', 'w')
f.write(str(lla2))
f.close()

# ampere l3
resp = client.read_input_registers(0x0A,2, unit=sdmid)
lla1 = float(struct.unpack('>f',struct.pack('>HH',*resp.registers))[0])
lla3 = float("%.1f" % lla1)
f = open('/var/www/html/openWB/ramdisk/pva3', 'w')
f.write(str(lla3))
f.close()

resp = client.read_input_registers(0x0156,2, unit=sdmid)
pvkwh = struct.unpack('>f',struct.pack('>HH',*resp.registers))[0]
pvkwh = float("%.3f" % pvkwh) * 1000
f = open('/var/www/html/openWB/ramdisk/pvkwh', 'w')
f.write(str(pvkwh))
f.close()
