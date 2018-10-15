#!/usr/bin/python
import sys
import os
import time
import getopt
import socket
import ConfigParser
import struct
import binascii
seradd = str(sys.argv[1])
from pymodbus.client.sync import ModbusSerialClient
client = ModbusSerialClient(method = "rtu", port=seradd, baudrate=9600,
                                stopbits=1, bytesize=8, timeout=1)


sdmid = int(sys.argv[2])

resp = client.read_input_registers(0x0002,2, unit=sdmid)
ikwh = resp.registers[1]
ikwh = float(ikwh) /100
f = open('/var/www/html/openWB/ramdisk/llkwhs1', 'w')
f.write(str(ikwh))
f.close()

resp = client.read_input_registers(0x0E,2, unit=sdmid)
lla1 = resp.registers[1]
lla1 = float(lla1) / 100
f = open('/var/www/html/openWB/ramdisk/llas11', 'w')
f.write(str(lla1))
f.close()

resp = client.read_input_registers(0x10,2, unit=sdmid)
lla2 = resp.registers[1]
lla2 = float(lla2) / 100
f = open('/var/www/html/openWB/ramdisk/llas12', 'w')
f.write(str(lla2))
f.close()

resp = client.read_input_registers(0x12,2, unit=sdmid)
lla3 = resp.registers[1]
lla3 = float(lla3) / 100
f = open('/var/www/html/openWB/ramdisk/llas13', 'w')
f.write(str(lla3))
f.close()


resp = client.read_input_registers(0x26,2, unit=sdmid)
s = str(struct.unpack('<hh',struct.pack('<HH',*resp.registers)))
ss = s.split(", ")[1].split(")")[0]
ss = int(ss) / 100
f = open('/var/www/html/openWB/ramdisk/llaktuells1', 'w')
f.write(str(ss))
f.close()

resp = client.read_input_registers(0x08,4, unit=sdmid)
voltage = resp.registers[1]
voltage = float(voltage) / 10
f = open('/var/www/html/openWB/ramdisk/llvs11', 'w')
f.write(str(voltage))
f.close()

resp = client.read_input_registers(0x0A,4, unit=sdmid)
voltage = resp.registers[1]
voltage = float(voltage) / 10
f = open('/var/www/html/openWB/ramdisk/llvs12', 'w')
f.write(str(voltage))
f.close()

resp = client.read_input_registers(0x0C,4, unit=sdmid)
voltage = resp.registers[1]
voltage = float(voltage) / 10
f = open('/var/www/html/openWB/ramdisk/llvs13', 'w')
f.write(str(voltage))
f.close()

