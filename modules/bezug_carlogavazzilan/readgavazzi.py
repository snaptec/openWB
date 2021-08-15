#!/usr/bin/python 
import sys 
# import os 
# import time 
# import getopt 
import struct 
from pymodbus.client.sync import ModbusTcpClient 

ipadd = str(sys.argv[1])

client = ModbusTcpClient(ipadd, port=502) 
sdmid = 1 

#Voltage
resp = client.read_input_registers(0x00,2, unit=sdmid)
all = format(resp.registers[1], '04x') + format(resp.registers[0], '04x')
voltage1 = float(struct.unpack('>i', all.decode('hex'))[0])
voltage1 = float("%.1f" % voltage1) / 10
f = open('/var/www/html/openWB/ramdisk/evuv1', 'w')
f.write(str(voltage1))
f.close()

resp = client.read_input_registers(0x02,2, unit=sdmid)
all = format(resp.registers[1], '04x') + format(resp.registers[0], '04x')
voltage2 = float(struct.unpack('>i', all.decode('hex'))[0])
voltage2 = float("%.1f" % voltage2) / 10
f = open('/var/www/html/openWB/ramdisk/evuv2', 'w')
f.write(str(voltage2))
f.close()

resp = client.read_input_registers(0x04,2, unit=sdmid)
all = format(resp.registers[1], '04x') + format(resp.registers[0], '04x')
voltage3 = float(struct.unpack('>i', all.decode('hex'))[0])
voltage3 = float("%.1f" % voltage3) / 10
f = open('/var/www/html/openWB/ramdisk/evuv3', 'w')
f.write(str(voltage3))
f.close()

#phasen watt
resp = client.read_input_registers(0x12,2, unit=sdmid)
all = format(resp.registers[1], '04x') + format(resp.registers[0], '04x')
finalw1 = int(struct.unpack('>i', all.decode('hex'))[0] / 10)

f = open('/var/www/html/openWB/ramdisk/bezugw1', 'w')
f.write(str(finalw1))
f.close()
resp = client.read_input_registers(0x14,2, unit=sdmid)
all = format(resp.registers[1], '04x') + format(resp.registers[0], '04x')
finalw2 = int(struct.unpack('>i', all.decode('hex'))[0] / 10)

f = open('/var/www/html/openWB/ramdisk/bezugw2', 'w')
f.write(str(finalw2))
f.close()
resp = client.read_input_registers(0x16,2, unit=sdmid)
all = format(resp.registers[1], '04x') + format(resp.registers[0], '04x')
finalw3 = int(struct.unpack('>i', all.decode('hex'))[0] / 10)

f = open('/var/www/html/openWB/ramdisk/bezugw3', 'w')
f.write(str(finalw3))
f.close()
finalw= finalw1 + finalw2 + finalw3
f = open('/var/www/html/openWB/ramdisk/wattbezug', 'w')
f.write(str(finalw))
f.close()

#ampere l1
resp = client.read_input_registers(0x0C,2, unit=sdmid)
all = format(resp.registers[1], '04x') + format(resp.registers[0], '04x')
lla1 = float(struct.unpack('>i', all.decode('hex'))[0])
lla1 = float("%.1f" % lla1) / 1000
f = open('/var/www/html/openWB/ramdisk/bezuga1', 'w')
if finalw1 < 0:
    f.write(str(-lla1))
else:
    f.write(str(lla1))
f.close()

#ampere l2
resp = client.read_input_registers(0x0E,2, unit=sdmid)
all = format(resp.registers[1], '04x') + format(resp.registers[0], '04x')
lla1 = float(struct.unpack('>i', all.decode('hex'))[0])
lla2 = float("%.1f" % lla1) / 1000
f = open('/var/www/html/openWB/ramdisk/bezuga2', 'w')
if finalw2 < 0:
    f.write(str(-lla2))
else:
    f.write(str(lla2))
f.close()

#ampere l3
resp = client.read_input_registers(0x10,2, unit=sdmid)
all = format(resp.registers[1], '04x') + format(resp.registers[0], '04x')
lla1 = float(struct.unpack('>i', all.decode('hex'))[0])
lla3 = float("%.1f" % lla1) / 1000
f = open('/var/www/html/openWB/ramdisk/bezuga3', 'w')
if finalw3 < 0:
    f.write(str(-lla3))
else:
    f.write(str(lla3))
f.close()

#evuhz
resp = client.read_input_registers(0x33,2, unit=sdmid)
hz = resp.registers[0] / 10
evuhz = float("%.2f" % hz)
if evuhz > 100:
    evuhz=float(evuhz / 10)
f = open('/var/www/html/openWB/ramdisk/evuhz', 'w')
f.write(str(evuhz))
f.close()
