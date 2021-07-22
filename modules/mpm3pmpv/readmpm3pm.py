#!/usr/bin/python
import sys
# import os
# import time
# import getopt
# import socket
# import ConfigParser
import struct
# import binascii
from pymodbus.client.sync import ModbusSerialClient

seradd = str(sys.argv[1])
sdmid = int(sys.argv[2])

client = ModbusSerialClient(method = "rtu", port=seradd, baudrate=9600, stopbits=1, bytesize=8, timeout=1)

resp = client.read_input_registers(0x0004,4, unit=sdmid)
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

resp = client.read_input_registers(0x0E,2, unit=sdmid)
lla1 = resp.registers[1]
lla1 = float(lla1) / 100
f = open('/var/www/html/openWB/ramdisk/pva1', 'w')
f.write(str(lla1))
f.close()

resp = client.read_input_registers(0x10,2, unit=sdmid)
lla2 = resp.registers[1]
lla2 = float(lla2) / 100
f = open('/var/www/html/openWB/ramdisk/pva2', 'w')
f.write(str(lla2))
f.close()

resp = client.read_input_registers(0x12,2, unit=sdmid)
lla3 = resp.registers[1]
lla3 = float(lla3) / 100
f = open('/var/www/html/openWB/ramdisk/pva3', 'w')
f.write(str(lla3))
f.close()

# total watt
resp = client.read_input_registers(0x26,2, unit=sdmid)
value1 = resp.registers[0] 
value2 = resp.registers[1] 
all = format(value1, '04x') + format(value2, '04x')
final = int(struct.unpack('>i', all.decode('hex'))[0]) / 100
f = open('/var/www/html/openWB/ramdisk/pvwatt', 'w')
f.write(str(final))
f.close()
