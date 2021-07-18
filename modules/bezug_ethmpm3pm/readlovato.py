#!/usr/bin/python
# import sys
# import os
# import time
# import getopt
import struct
from pymodbus.client.sync import ModbusTcpClient

client = ModbusTcpClient('192.168.193.15', port=8899)

#Voltage
resp = client.read_input_registers(0x0001,2, unit=0x02)
voltage1 = float(resp.registers[1] / 100)
f = open('/var/www/html/openWB/ramdisk/evuv1', 'w')
f.write(str(voltage1))
f.close()
resp = client.read_input_registers(0x0003,2, unit=0x02)
voltage2 = float(resp.registers[1] / 100)
f = open('/var/www/html/openWB/ramdisk/evuv2', 'w')
f.write(str(voltage2))
f.close()
resp = client.read_input_registers(0x0005,2, unit=0x02)
voltage3 = float(resp.registers[1] / 100)
f = open('/var/www/html/openWB/ramdisk/evuv3', 'w')
f.write(str(voltage3))
f.close()

#phasen watt
resp = client.read_input_registers(0x0013,2, unit=0x02)
all = format(resp.registers[0], '04x') + format(resp.registers[1], '04x')
finalw1 = int(struct.unpack('>i', all.decode('hex'))[0] / 100)
f = open('/var/www/html/openWB/ramdisk/bezugw1', 'w')
f.write(str(finalw1))
f.close()
resp = client.read_input_registers(0x0015,2, unit=0x02)
all = format(resp.registers[0], '04x') + format(resp.registers[1], '04x')
finalw2 = int(struct.unpack('>i', all.decode('hex'))[0] / 100)
f = open('/var/www/html/openWB/ramdisk/bezugw2', 'w')
f.write(str(finalw2))
f.close()
resp = client.read_input_registers(0x0017,2, unit=0x02)
all = format(resp.registers[0], '04x') + format(resp.registers[1], '04x')
finalw3 = int(struct.unpack('>i', all.decode('hex'))[0] / 100)
f = open('/var/www/html/openWB/ramdisk/bezugw3', 'w')
f.write(str(finalw3))
f.close()

finalw= finalw1 + finalw2 + finalw3
# total watt
# resp = client.read_input_registers(0x0039,2, unit=0x02)
# all = format(resp.registers[0], '04x') + format(resp.registers[1], '04x')
# finalw = int(struct.unpack('>i', all.decode('hex'))[0] / 100)
f = open('/var/www/html/openWB/ramdisk/wattbezug', 'w')
f.write(str(finalw))
f.close()

#ampere l1
resp = client.read_input_registers(0x0007, 2, unit=0x02)
all = format(resp.registers[0], '04x') + format(resp.registers[1], '04x')
lla1 = float(struct.unpack('>i', all.decode('hex'))[0]) / 10000
f = open('/var/www/html/openWB/ramdisk/bezuga1', 'w')
if finalw1 < 0:
    f.write(str(-lla1))
else:
    f.write(str(lla1))
f.close()

#ampere l2
resp = client.read_input_registers(0x0009, 2, unit=0x02)
all = format(resp.registers[0], '04x') + format(resp.registers[1], '04x')
lla2 = float(struct.unpack('>i', all.decode('hex'))[0]) / 10000
f = open('/var/www/html/openWB/ramdisk/bezuga2', 'w')
if finalw2 < 0:
    f.write(str(-lla2))
else:
    f.write(str(lla2))
f.close()

#ampere l3
resp = client.read_input_registers(0x000b, 2, unit=0x02)
all = format(resp.registers[0], '04x') + format(resp.registers[1], '04x')
lla3 = float(struct.unpack('>i', all.decode('hex'))[0]) / 10000
f = open('/var/www/html/openWB/ramdisk/bezuga3', 'w')
if finalw3 < 0:
    f.write(str(-lla3))
else:
    f.write(str(lla3))
f.close()

#evuhz
resp = client.read_input_registers(0x0031,2, unit=0x02)
evuhz= float(resp.registers[1])
evuhz= float(evuhz / 100)
if evuhz > 100:
    evuhz=float(evuhz / 10)
f = open('/var/www/html/openWB/ramdisk/evuhz', 'w')
f.write(str(evuhz))
f.close()

#Power Factor
resp = client.read_input_registers(0x0025,2, unit=0x02)
evupf1 = float(resp.registers[1]) / 10000
f = open('/var/www/html/openWB/ramdisk/evupf1', 'w')
f.write(str(evupf1))
f.close()

resp = client.read_input_registers(0x0027,2, unit=0x02)
evupf2 = float(resp.registers[1]) / 10000
f = open('/var/www/html/openWB/ramdisk/evupf2', 'w')
f.write(str(evupf2))
f.close()

resp = client.read_input_registers(0x0029,2, unit=0x02)
evupf3 = float(resp.registers[1]) / 10000
f = open('/var/www/html/openWB/ramdisk/evupf3', 'w')
f.write(str(evupf3))
f.close()
