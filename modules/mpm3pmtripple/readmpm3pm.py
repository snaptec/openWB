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
idadd = int(sys.argv[2])

client = ModbusSerialClient(method = "rtu", port=seradd, baudrate=9600, stopbits=1, bytesize=8, timeout=1)

resp = client.read_input_registers(0x00,2, unit=idadd)
voltage = struct.unpack('>f',struct.pack('>HH',*resp.registers))[0]
voltage = float("%.1f" % voltage)
f = open('/var/www/html/openWB/ramdisk/llv1', 'w')
f.write(str(voltage))
f.close()
resp = client.read_input_registers(0x06,2, unit=idadd)
lla1 = float(struct.unpack('>f',struct.pack('>HH',*resp.registers))[0])
lla1 = float("%.1f" % lla1)
f = open('/var/www/html/openWB/ramdisk/lla1', 'w')
f.write(str(lla1))
f.close()
resp = client.read_input_registers(0x08,2, unit=idadd)
lla2 = float(struct.unpack('>f',struct.pack('>HH',*resp.registers))[0])
lla2 = float("%.1f" % lla2)
f = open('/var/www/html/openWB/ramdisk/llas11', 'w')
f.write(str(lla2))
f.close()
resp = client.read_input_registers(0x0A,2, unit=idadd)
lla3 = struct.unpack('>f',struct.pack('>HH',*resp.registers))[0]
lla3 = float("%.1f" % lla3)
f = open('/var/www/html/openWB/ramdisk/llas21', 'w')
f.write(str(lla3))
f.close()
resp = client.read_input_registers(0x0C,2, unit=idadd)
llw1 = struct.unpack('>f',struct.pack('>HH',*resp.registers))[0]
llw1 = int(llw1)
if llw1 < 15:
    llw1 = 0
f = open('/var/www/html/openWB/ramdisk/llaktuell', 'w')
f.write(str(llw1))
f.close()

resp = client.read_input_registers(0x015A,2, unit=idadd)
llkwh = struct.unpack('>f',struct.pack('>HH',*resp.registers))[0]
llkwh = float("%.3f" % llkwh)
f = open('/var/www/html/openWB/ramdisk/llkwh', 'w')
f.write(str(llkwh))
f.close()
resp = client.read_input_registers(0x015C,2, unit=idadd)
llkwh = struct.unpack('>f',struct.pack('>HH',*resp.registers))[0]
llkwh = float("%.3f" % llkwh)
f = open('/var/www/html/openWB/ramdisk/llkwhs1', 'w')
f.write(str(llkwh))
f.close()
resp = client.read_input_registers(0x015E,2, unit=idadd)
llkwh = struct.unpack('>f',struct.pack('>HH',*resp.registers))[0]
llkwh = float("%.3f" % llkwh)
f = open('/var/www/html/openWB/ramdisk/llkwhs2', 'w')
f.write(str(llkwh))
f.close()
resp = client.read_input_registers(0x0E,2, unit=idadd)
llw2 = struct.unpack('>f',struct.pack('>HH',*resp.registers))[0]
llw2 = int(llw2)
if llw2 < 15:
    llw2 = 0
f = open('/var/www/html/openWB/ramdisk/llaktuells1', 'w')
f.write(str(llw2))
f.close()

resp = client.read_input_registers(0x10,2, unit=idadd)
llw3 = struct.unpack('>f',struct.pack('>HH',*resp.registers))[0]
llw3 = int(llw3)
if llw3 < 15:
    llw3 = 0
f = open('/var/www/html/openWB/ramdisk/llaktuells2', 'w')
f.write(str(llw3))
f.close()

resp = client.read_input_registers(0x02,2, unit=idadd)
voltage = struct.unpack('>f',struct.pack('>HH',*resp.registers))[0]
voltage = float("%.1f" % voltage)
f = open('/var/www/html/openWB/ramdisk/llvs11', 'w')
f.write(str(voltage))
f.close() 
resp = client.read_input_registers(0x04,2, unit=idadd)
voltage = struct.unpack('>f',struct.pack('>HH',*resp.registers))[0]
voltage = float("%.1f" % voltage)
f = open('/var/www/html/openWB/ramdisk/llvs21', 'w')
f.write(str(voltage))
f.close()
