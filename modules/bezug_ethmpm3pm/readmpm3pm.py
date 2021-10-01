#!/usr/bin/python
# import sys
# import os
# import time
# import getopt
import struct
from pymodbus.client.sync import ModbusTcpClient

client = ModbusTcpClient('192.168.193.15', port=8899)

# Voltage
resp = client.read_input_registers(0x08,4, unit=5)
voltage1 = resp.registers[1]
voltage1 = float(voltage1) / 10
f = open('/var/www/html/openWB/ramdisk/evuv1', 'w')
f.write(str(voltage1))
f.close()

resp = client.read_input_registers(0x0A,4, unit=5)
voltage2 = resp.registers[1]
voltage2 = float(voltage2) / 10
f = open('/var/www/html/openWB/ramdisk/evuv2', 'w')
f.write(str(voltage2))
f.close()

resp = client.read_input_registers(0x0C,4, unit=5)
voltage3 = resp.registers[1]
voltage3 = float(voltage3) / 10
f = open('/var/www/html/openWB/ramdisk/evuv3', 'w')
f.write(str(voltage3))
f.close()

resp = client.read_input_registers(0x0002,4, unit=5)
value1 = resp.registers[0] 
value2 = resp.registers[1] 
all = format(value1, '04x') + format(value2, '04x')
ikwh = int(struct.unpack('>i', all.decode('hex'))[0]) 
ikwh = float(ikwh) * 10
f = open('/var/www/html/openWB/ramdisk/bezugkwh', 'w')
f.write(str(ikwh))
f.close()

# phasen watt
resp = client.read_input_registers(0x14,2, unit=5)
value1 = resp.registers[0] 
value2 = resp.registers[1] 
all = format(value1, '04x') + format(value2, '04x')
finalw1 = int(struct.unpack('>i', all.decode('hex'))[0]) / 100
f = open('/var/www/html/openWB/ramdisk/bezugw1', 'w')
f.write(str(finalw1))
f.close()
resp = client.read_input_registers(0x16,2, unit=5)
value1 = resp.registers[0] 
value2 = resp.registers[1] 
all = format(value1, '04x') + format(value2, '04x')
finalw2 = int(struct.unpack('>i', all.decode('hex'))[0]) / 100
f = open('/var/www/html/openWB/ramdisk/bezugw2', 'w')
f.write(str(finalw2))
f.close()
resp = client.read_input_registers(0x18,2, unit=5)
value1 = resp.registers[0] 
value2 = resp.registers[1] 
all = format(value1, '04x') + format(value2, '04x')
finalw3 = int(struct.unpack('>i', all.decode('hex'))[0]) / 100
f = open('/var/www/html/openWB/ramdisk/bezugw3', 'w')
f.write(str(finalw3))
f.close()

# resp = client.read_input_registers(0x0E,2, unit=5)
# lla1 = resp.registers[1]
# lla1 = float(lla1) / 100
lla1=round(float(float(finalw1) / float(voltage1)), 2)
f = open('/var/www/html/openWB/ramdisk/bezuga1', 'w')
f.write(str(lla1))
f.close()

# resp = client.read_input_registers(0x10,2, unit=5)
# lla2 = resp.registers[1]
# lla2 = float(lla2) / 100
lla2=round(float(float(finalw2) / float(voltage2)), 2)
f = open('/var/www/html/openWB/ramdisk/bezuga2', 'w')
f.write(str(lla2))
f.close()

# resp = client.read_input_registers(0x12,2, unit=5)
# lla3 = resp.registers[1]
# lla3 = float(lla3) / 100
lla3=round(float(float(finalw3) / float(voltage3)), 2) 
f = open('/var/www/html/openWB/ramdisk/bezuga3', 'w')
f.write(str(lla3))
f.close()

# total watt
resp = client.read_input_registers(0x26,2, unit=5)
value1 = resp.registers[0] 
value2 = resp.registers[1] 
all = format(value1, '04x') + format(value2, '04x')
final = int(struct.unpack('>i', all.decode('hex'))[0]) / 100
f = open('/var/www/html/openWB/ramdisk/wattbezug', 'w')
f.write(str(final))
f.close()

# export kwh
resp = client.read_input_registers(0x0004,4, unit=5)
value1 = resp.registers[0] 
value2 = resp.registers[1] 
all = format(value1, '04x') + format(value2, '04x')
ekwh = int(struct.unpack('>i', all.decode('hex'))[0]) 
ekwh = float(ekwh) * 10
f = open('/var/www/html/openWB/ramdisk/einspeisungkwh', 'w')
f.write(str(ekwh))
f.close()

# evuhz
resp = client.read_input_registers(0x2c,4, unit=5)
value1 = resp.registers[0] 
value2 = resp.registers[1] 
all = format(value1, '04x') + format(value2, '04x')
hz = int(struct.unpack('>i', all.decode('hex'))[0]) 
hz = round((float(hz) / 100), 2)
f = open('/var/www/html/openWB/ramdisk/evuhz', 'w')
f.write(str(hz))
f.close()

# Power Factor
resp = client.read_input_registers(0x20,4, unit=5)
value1 = resp.registers[0] 
value2 = resp.registers[1]
all = format(value1, '04x') + format(value2, '04x')
evupf1 = int(struct.unpack('>i', all.decode('hex'))[0]) 
evupf1 = round((float(evupf1) / 10), 0)
f = open('/var/www/html/openWB/ramdisk/evupf1', 'w')
f.write(str(evupf1))
f.close()

resp = client.read_input_registers(0x22,4, unit=5)
value1 = resp.registers[0] 
value2 = resp.registers[1]
all = format(value1, '04x') + format(value2, '04x')
evupf2 = int(struct.unpack('>i', all.decode('hex'))[0]) 
evupf2 = round((float(evupf2) / 10), 0)
f = open('/var/www/html/openWB/ramdisk/evupf2', 'w')
f.write(str(evupf2))
f.close()

resp = client.read_input_registers(0x24,4, unit=5)
value1 = resp.registers[0] 
value2 = resp.registers[1]
all = format(value1, '04x') + format(value2, '04x')
evupf3 = int(struct.unpack('>i', all.decode('hex'))[0]) 
evupf3 = round((float(evupf3) / 10), 0)
f = open('/var/www/html/openWB/ramdisk/evupf3', 'w')
f.write(str(evupf3))
f.close()
