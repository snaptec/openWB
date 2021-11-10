#!/usr/bin/python
# import sys
# import os
# import time
# import getopt
import struct
from pymodbus.client.sync import ModbusTcpClient

client = ModbusTcpClient('192.168.193.15', port=8899)

resp = client.read_input_registers(0x0004,4, unit=8)
value1 = resp.registers[0] 
value2 = resp.registers[1] 
all = format(value1, '04x') + format(value2, '04x')
ikwh = int(struct.unpack('>i', all.decode('hex'))[0]) 

# resp = client.read_input_registers(0x0004,2, unit=sdmid)
# ikwh = resp.registers[1]
ikwh = float(ikwh) * 10
f = open('/var/www/html/openWB/ramdisk/pvkwh', 'w')
f.write(str(ikwh))
f.close()
pvkwhk= ikwh / 1000
f = open('/var/www/html/openWB/ramdisk/pvkwhk', 'w')
f.write(str(pvkwhk))
f.close()

ikwhk = float(ikwh) / 1000
f = open('/var/www/html/openWB/ramdisk/pvkwhk', 'w')
f.write(str(ikwhk))
f.close()

resp = client.read_input_registers(0x0E,2, unit=8)
lla1 = resp.registers[1]
lla1 = float(lla1) / 100
f = open('/var/www/html/openWB/ramdisk/pva1', 'w')
f.write(str(lla1))
f.close()

resp = client.read_input_registers(0x10,2, unit=8)
lla2 = resp.registers[1]
lla2 = float(lla2) / 100
f = open('/var/www/html/openWB/ramdisk/pva2', 'w')
f.write(str(lla2))
f.close()

resp = client.read_input_registers(0x12,2, unit=8)
lla3 = resp.registers[1]
lla3 = float(lla3) / 100
f = open('/var/www/html/openWB/ramdisk/pva3', 'w')
f.write(str(lla3))
f.close()

# total watt
resp = client.read_input_registers(0x26,2, unit=8)
value1 = resp.registers[0] 
value2 = resp.registers[1] 
all = format(value1, '04x') + format(value2, '04x')
final = int(struct.unpack('>i', all.decode('hex'))[0]) / 100
f = open('/var/www/html/openWB/ramdisk/pvwatt', 'w')
f.write(str(final))
f.close()
