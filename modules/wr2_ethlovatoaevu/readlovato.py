#!/usr/bin/python
# import sys
# import os
# import time
# import getopt
import struct
from pymodbus.client.sync import ModbusTcpClient

client = ModbusTcpClient('192.168.193.15', port=8899)

# Counters
resp = client.read_input_registers(0x1a1f,2, unit=0x08)
all = format(resp.registers[0], '04x') + format(resp.registers[1], '04x')
finalbezug = int(struct.unpack('>i', all.decode('hex'))[0])
f = open('/var/www/html/openWB/ramdisk/pv2kwh', 'w')
f.write(str(finalbezug))
f.close()

# phasen watt
resp = client.read_input_registers(0x0013,2, unit=0x08)
all = format(resp.registers[0], '04x') + format(resp.registers[1], '04x')
finalw1 = int(struct.unpack('>i', all.decode('hex'))[0] / 100)
resp = client.read_input_registers(0x0015,2, unit=0x08)
all = format(resp.registers[0], '04x') + format(resp.registers[1], '04x')
finalw2 = int(struct.unpack('>i', all.decode('hex'))[0] / 100)
resp = client.read_input_registers(0x0017,2, unit=0x08)
all = format(resp.registers[0], '04x') + format(resp.registers[1], '04x')
finalw3 = int(struct.unpack('>i', all.decode('hex'))[0] / 100)

finalw= finalw1 + finalw2 + finalw3
if ( finalw > 10):
    finalw=finalw*-1
# total watt
# resp = client.read_input_registers(0x0039,2, unit=0x08)
# all = format(resp.registers[0], '04x') + format(resp.registers[1], '04x')
# finalw = int(struct.unpack('>i', all.decode('hex'))[0] / 100)
f = open('/var/www/html/openWB/ramdisk/pv2watt', 'w')
f.write(str(finalw))
f.close()

# ampere l1
resp = client.read_input_registers(0x0007, 2, unit=0x08)
all = format(resp.registers[0], '04x') + format(resp.registers[1], '04x')
lla1 = float(struct.unpack('>i', all.decode('hex'))[0]) / 10000
f = open('/var/www/html/openWB/ramdisk/pv2a1', 'w')
f.write(str(lla1))
f.close()

# ampere l2
resp = client.read_input_registers(0x0009, 2, unit=0x08)
all = format(resp.registers[0], '04x') + format(resp.registers[1], '04x')
lla2 = float(struct.unpack('>i', all.decode('hex'))[0]) / 10000
f = open('/var/www/html/openWB/ramdisk/pv2a2', 'w')
f.write(str(lla2))
f.close()

# ampere l3
resp = client.read_input_registers(0x000b, 2, unit=0x08)
all = format(resp.registers[0], '04x') + format(resp.registers[1], '04x')
lla3 = float(struct.unpack('>i', all.decode('hex'))[0]) / 10000
f = open('/var/www/html/openWB/ramdisk/pv2a3', 'w')
f.write(str(lla3))
f.close()
