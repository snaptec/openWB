#!/usr/bin/python
# import sys
# import os
# import time
# import getopt
import struct
from pymodbus.client.sync import ModbusTcpClient

client = ModbusTcpClient('192.168.193.19', port=8899)

resp = client.read_input_registers(0x0002,4, unit=1)
value1 = resp.registers[0] 
value2 = resp.registers[1] 
all = format(value1, '04x') + format(value2, '04x')
ikwh = int(struct.unpack('>i', all.decode('hex'))[0]) 
ikwh = float(ikwh) * 10
f = open('/var/www/html/openWB/ramdisk/speicherikwh', 'w')
f.write(str(ikwh))
f.close()

# total watt
resp = client.read_input_registers(0x26,2, unit=1)
value1 = resp.registers[0] 
value2 = resp.registers[1] 
all = format(value1, '04x') + format(value2, '04x')
final = int(struct.unpack('>i', all.decode('hex'))[0]) / 100
f = open('/var/www/html/openWB/ramdisk/speicherleistung', 'w')
f.write(str(final))
f.close()

# export kwh
resp = client.read_input_registers(0x0004,4, unit=1)
value1 = resp.registers[0] 
value2 = resp.registers[1] 
all = format(value1, '04x') + format(value2, '04x')
ekwh = int(struct.unpack('>i', all.decode('hex'))[0]) 
ekwh = float(ekwh) * 10
f = open('/var/www/html/openWB/ramdisk/speicherekwh', 'w')
f.write(str(ekwh))
f.close()
