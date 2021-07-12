#!/usr/bin/python
# import sys
# import os
# import time
# import getopt
# import socket
# import ConfigParser
import struct
# import binascii
from pymodbus.transaction import ModbusRtuFramer
from pymodbus.client.sync import ModbusTcpClient

client = ModbusTcpClient('192.168.193.18', port=8899, framer=ModbusRtuFramer)

resp = client.read_input_registers(0x0002,4, unit=5)
value1 = resp.registers[0] 
value2 = resp.registers[1] 
all = format(value1, '04x') + format(value2, '04x')
ikwh = int(struct.unpack('>i', all.decode('hex'))[0]) 
#resp = client.read_input_registers(0x0002,2, unit=5)
#ikwh = resp.registers[1]
ikwh = float(ikwh) /100
f = open('/var/www/html/openWB/ramdisk/llkwh', 'w')
f.write(str(ikwh))
f.close()

resp = client.read_input_registers(0x0E,2, unit=5)
lla1 = resp.registers[1]
lla1 = float(lla1) / 100
f = open('/var/www/html/openWB/ramdisk/lla1', 'w')
f.write(str(lla1))
f.close()

resp = client.read_input_registers(0x10,2, unit=5)
lla2 = resp.registers[1]
lla2 = float(lla2) / 100
f = open('/var/www/html/openWB/ramdisk/lla2', 'w')
f.write(str(lla2))
f.close()

resp = client.read_input_registers(0x12,2, unit=5)
lla3 = resp.registers[1]
lla3 = float(lla3) / 100
f = open('/var/www/html/openWB/ramdisk/lla3', 'w')
f.write(str(lla3))
f.close()

resp = client.read_input_registers(0x26,2, unit=5)
value1 = resp.registers[0] 
value2 = resp.registers[1] 
all = format(value1, '04x') + format(value2, '04x')
final = int(struct.unpack('>i', all.decode('hex'))[0]) / 100
if final < 10:
    final = 0
f = open('/var/www/html/openWB/ramdisk/llaktuell', 'w')
f.write(str(final))
f.close()

resp = client.read_input_registers(0x08,4, unit=5)
voltage = resp.registers[1]
voltage = float(voltage) / 10
f = open('/var/www/html/openWB/ramdisk/llv1', 'w')
f.write(str(voltage))
f.close()

resp = client.read_input_registers(0x0A,4, unit=5)
voltage = resp.registers[1]
voltage = float(voltage) / 10
f = open('/var/www/html/openWB/ramdisk/llv2', 'w')
f.write(str(voltage))
f.close()

resp = client.read_input_registers(0x0C,4, unit=5)
voltage = resp.registers[1]
voltage = float(voltage) / 10
f = open('/var/www/html/openWB/ramdisk/llv3', 'w')
f.write(str(voltage))
f.close()
