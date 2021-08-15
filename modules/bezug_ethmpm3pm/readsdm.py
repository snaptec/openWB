#!/usr/bin/python
# import sys
# import os
# import time
# import getopt
import struct
from pymodbus.client.sync import ModbusTcpClient

client = ModbusTcpClient('192.168.193.15', port=8899)
sdmid = 115

# Voltage
resp = client.read_input_registers(0x00,2, unit=sdmid)
voltage = struct.unpack('>f',struct.pack('>HH',*resp.registers))[0]
voltage1 = float("%.1f" % voltage)
f = open('/var/www/html/openWB/ramdisk/evuv1', 'w')
f.write(str(voltage1))
f.close()
resp = client.read_input_registers(0x02,2, unit=sdmid)
voltage = struct.unpack('>f',struct.pack('>HH',*resp.registers))[0]
voltage2 = float("%.1f" % voltage)
f = open('/var/www/html/openWB/ramdisk/evuv2', 'w')
f.write(str(voltage2))
f.close()
resp = client.read_input_registers(0x04,2, unit=sdmid)
voltage = struct.unpack('>f',struct.pack('>HH',*resp.registers))[0]
voltage3 = float("%.1f" % voltage)
f = open('/var/www/html/openWB/ramdisk/evuv3', 'w')
f.write(str(voltage3))
f.close()

# phasen watt
resp = client.read_input_registers(0x0C,2, unit=sdmid)
llw1 = struct.unpack('>f',struct.pack('>HH',*resp.registers))[0]
finalw1 = int(llw1)
f = open('/var/www/html/openWB/ramdisk/bezugw1', 'w')
f.write(str(finalw1))
f.close()
resp = client.read_input_registers(0x0E,2, unit=sdmid)
llw1 = struct.unpack('>f',struct.pack('>HH',*resp.registers))[0]
finalw2 = int(llw1)
f = open('/var/www/html/openWB/ramdisk/bezugw2', 'w')
f.write(str(finalw2))
f.close()
resp = client.read_input_registers(0x10,2, unit=sdmid)
llw1 = struct.unpack('>f',struct.pack('>HH',*resp.registers))[0]
finalw3 = int(llw1)
f = open('/var/www/html/openWB/ramdisk/bezugw3', 'w')
f.write(str(finalw3))
f.close()

finalw= finalw1 + finalw2 + finalw3
f = open('/var/www/html/openWB/ramdisk/wattbezug', 'w')
f.write(str(finalw))
f.close()

# ampere l1
resp = client.read_input_registers(0x06,2, unit=sdmid)
lla1 = float(struct.unpack('>f',struct.pack('>HH',*resp.registers))[0])
lla1 = float("%.1f" % lla1)
f = open('/var/www/html/openWB/ramdisk/bezuga1', 'w')
if finalw1 < 0:
    f.write(str(-lla1))
else:
    f.write(str(lla1))
f.close()

# ampere l2
resp = client.read_input_registers(0x08,2, unit=sdmid)
lla1 = float(struct.unpack('>f',struct.pack('>HH',*resp.registers))[0])
lla2 = float("%.1f" % lla1)
f = open('/var/www/html/openWB/ramdisk/bezuga2', 'w')
if finalw2 < 0:
    f.write(str(-lla2))
else:
    f.write(str(lla2))
f.close()

# ampere l3
resp = client.read_input_registers(0x0A,2, unit=sdmid)
lla1 = float(struct.unpack('>f',struct.pack('>HH',*resp.registers))[0])
lla3 = float("%.1f" % lla1)
f = open('/var/www/html/openWB/ramdisk/bezuga3', 'w')
if finalw3 < 0:
    f.write(str(-lla3))
else:
    f.write(str(lla3))
f.close()

# evuhz
resp = client.read_input_registers(0x46,2, unit=sdmid)
hz = struct.unpack('>f',struct.pack('>HH',*resp.registers))[0]
evuhz = float("%.2f" % hz)
if evuhz > 100:
    evuhz=float(evuhz / 10)
f = open('/var/www/html/openWB/ramdisk/evuhz', 'w')
f.write(str(evuhz))
f.close()

# Power Factor
resp = client.read_input_registers(0x1E,2, unit=sdmid)
evu1pf = struct.unpack('>f',struct.pack('>HH',*resp.registers))[0]
evu1pf = float("%.2f" % evu1pf)
f = open('/var/www/html/openWB/ramdisk/evupf1', 'w')
f.write(str(evu1pf))
f.close()

resp = client.read_input_registers(0x20,2, unit=sdmid)
evu2pf = struct.unpack('>f',struct.pack('>HH',*resp.registers))[0]
evu2pf = float("%.2f" % evu2pf)
f = open('/var/www/html/openWB/ramdisk/evupf2', 'w')
f.write(str(evu2pf))
f.close()

resp = client.read_input_registers(0x22,2, unit=sdmid)
evu3pf = struct.unpack('>f',struct.pack('>HH',*resp.registers))[0]
evu3pf = float("%.2f" % evu3pf)
f = open('/var/www/html/openWB/ramdisk/evupf3', 'w')
f.write(str(evu3pf))
f.close()
