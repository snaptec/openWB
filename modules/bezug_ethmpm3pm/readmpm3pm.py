#!/usr/bin/python
import sys
import os
import time
import getopt
import struct
from pymodbus.client.sync import ModbusTcpClient
client = ModbusTcpClient('192.168.193.15', port=8899)
#from pymodbus.transaction import ModbusRtuFramer
#client = ModbusTcpClient('192.168.0.7', port=8899, framer=ModbusRtuFramer)




#Voltage
resp = client.read_input_registers(0x08,4, unit=5)
voltage = resp.registers[1]
voltage = float(voltage) / 10
f = open('/var/www/html/openWB/ramdisk/evuv1', 'w')
f.write(str(voltage))
f.close()

resp = client.read_input_registers(0x0A,4, unit=5)
voltage = resp.registers[1]
voltage = float(voltage) / 10
f = open('/var/www/html/openWB/ramdisk/evuv2', 'w')
f.write(str(voltage))
f.close()

resp = client.read_input_registers(0x0C,4, unit=5)
voltage = resp.registers[1]
voltage = float(voltage) / 10
f = open('/var/www/html/openWB/ramdisk/evuv3', 'w')
f.write(str(voltage))
f.close()

resp = client.read_input_registers(0x0002,4, unit=5)
value1 = resp.registers[0] 
value2 = resp.registers[1] 
all = format(value1, '04x') + format(value2, '04x')
ikwh = int(struct.unpack('>i', all.decode('hex'))[0]) 
ikwh = float(ekwh) * 10
f = open('/var/www/html/openWB/ramdisk/bezugkwh', 'w')
f.write(str(ikwh))
f.close()

resp = client.read_input_registers(0x0E,2, unit=5)
lla1 = resp.registers[1]
lla1 = float(lla1) / 100
f = open('/var/www/html/openWB/ramdisk/bezuga1', 'w')
f.write(str(lla1))
f.close()

resp = client.read_input_registers(0x10,2, unit=5)
lla2 = resp.registers[1]
lla2 = float(lla2) / 100
f = open('/var/www/html/openWB/ramdisk/bezuga2', 'w')
f.write(str(lla2))
f.close()

resp = client.read_input_registers(0x12,2, unit=5)
lla3 = resp.registers[1]
lla3 = float(lla3) / 100
f = open('/var/www/html/openWB/ramdisk/bezuga3', 'w')
f.write(str(lla3))
f.close()

#phasen watt
resp = client.read_input_registers(0x14,2, unit=5)
value1 = resp.registers[0] 
value2 = resp.registers[1] 
all = format(value1, '04x') + format(value2, '04x')
final = int(struct.unpack('>i', all.decode('hex'))[0]) / 100
f = open('/var/www/html/openWB/ramdisk/bezugw1', 'w')
f.write(str(final))
f.close()
resp = client.read_input_registers(0x16,2, unit=5)
value1 = resp.registers[0] 
value2 = resp.registers[1] 
all = format(value1, '04x') + format(value2, '04x')
final = int(struct.unpack('>i', all.decode('hex'))[0]) / 100
f = open('/var/www/html/openWB/ramdisk/bezugw2', 'w')
f.write(str(final))
f.close()
resp = client.read_input_registers(0x18,2, unit=5)
value1 = resp.registers[0] 
value2 = resp.registers[1] 
all = format(value1, '04x') + format(value2, '04x')
final = int(struct.unpack('>i', all.decode('hex'))[0]) / 100
f = open('/var/www/html/openWB/ramdisk/bezugw3', 'w')
f.write(str(final))
f.close()
#total watt
resp = client.read_input_registers(0x26,2, unit=5)
value1 = resp.registers[0] 
value2 = resp.registers[1] 
all = format(value1, '04x') + format(value2, '04x')
final = int(struct.unpack('>i', all.decode('hex'))[0]) / 100
f = open('/var/www/html/openWB/ramdisk/wattbezug', 'w')
f.write(str(final))
f.close()

#export kwh
resp = client.read_input_registers(0x0004,4, unit=5)
value1 = resp.registers[0] 
value2 = resp.registers[1] 
all = format(value1, '04x') + format(value2, '04x')
ekwh = int(struct.unpack('>i', all.decode('hex'))[0]) 
ekwh = float(ekwh) * 10
f = open('/var/www/html/openWB/ramdisk/einspeisungkwh', 'w')
f.write(str(ekwh))
f.close()

