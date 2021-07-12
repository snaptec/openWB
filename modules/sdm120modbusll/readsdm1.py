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

resp = client.read_input_registers(0x00,2, unit=sdmid)
llv1 = struct.unpack('>f',struct.pack('>HH',*resp.registers))
llv1 = float("%.1f" % llv1[0])
f = open('/var/www/html/openWB/ramdisk/llv1', 'w')
f.write(str(llv1))
f.close()

resp = client.read_input_registers(0x06,2, unit=sdmid)
lla1 = struct.unpack('>f',struct.pack('>HH',*resp.registers))
lla1 = float("%.3f" % lla1[0])
f = open('/var/www/html/openWB/ramdisk/lla1', 'w')
f.write(str(lla1))
f.close()

resp = client.read_input_registers(0x0C,2, unit=sdmid)
ll = struct.unpack('>f',struct.pack('>HH',*resp.registers))
ll = int(ll[0])
f = open('/var/www/html/openWB/ramdisk/llaktuell', 'w')
f.write(str(ll))
f.close()

resp = client.read_input_registers(0x1E,2, unit=sdmid)
llpf = struct.unpack('>f',struct.pack('>HH',*resp.registers))
llpf = float("%.3f" % llpf[0])
f = open('/var/www/html/openWB/ramdisk/llpf1', 'w')
f.write(str(llpf))
f.close()

resp = client.read_input_registers(0x0156,2, unit=sdmid)
llwh = struct.unpack('>f',struct.pack('>HH',*resp.registers))
llwh = float("%.3f" % llwh[0])
f = open('/var/www/html/openWB/ramdisk/llkwh', 'w')
f.write(str(llwh))
f.close()
