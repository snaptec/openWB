#!/usr/bin/python
import sys
# import os
import time
# import getopt
# import socket
# import ConfigParser
import struct
# import binascii
from pymodbus.client.sync import ModbusSerialClient

seradd = str(sys.argv[1])
sdmid  = int(sys.argv[2])
sdm2id = int(sys.argv[3])
sdm3id = int(sys.argv[4])

client = ModbusSerialClient(method = "rtu", port=seradd, baudrate=9600, stopbits=1, bytesize=8, timeout=1)

# rq = client.read_holding_registers(0,8,unit=5)
# print(rq.registers)
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
wl1 = int(ll[0])

resp = client.read_input_registers(0x0156,2, unit=sdmid)
llwh = struct.unpack('>f',struct.pack('>HH',*resp.registers))
llwh1 = float("%.3f" % llwh[0])
time.sleep(0.5)
resp = client.read_input_registers(0x00,2, unit=sdm2id)
llv2 = struct.unpack('>f',struct.pack('>HH',*resp.registers))
llv2 = float("%.1f" % llv2[0])
f = open('/var/www/html/openWB/ramdisk/llv2', 'w')
f.write(str(llv2))
f.close()
resp = client.read_input_registers(0x06,2, unit=sdm2id)
lla2 = struct.unpack('>f',struct.pack('>HH',*resp.registers))
lla2 = float("%.3f" % lla2[0])
f = open('/var/www/html/openWB/ramdisk/lla2', 'w')
f.write(str(lla2))
f.close()
resp = client.read_input_registers(0x0C,2, unit=sdm2id)
ll = struct.unpack('>f',struct.pack('>HH',*resp.registers))
wl2 = int(ll[0])
resp = client.read_input_registers(0x0156,2, unit=sdm2id)
llwh = struct.unpack('>f',struct.pack('>HH',*resp.registers))
llwh2 = float("%.3f" % llwh[0])
time.sleep(0.5)
resp = client.read_input_registers(0x00,2, unit=sdm3id)
llv3 = struct.unpack('>f',struct.pack('>HH',*resp.registers))
llv3 = float("%.1f" % llv3[0])
f = open('/var/www/html/openWB/ramdisk/llv3', 'w')
f.write(str(llv3))
f.close()
resp = client.read_input_registers(0x06,2, unit=sdm3id)
lla3 = struct.unpack('>f',struct.pack('>HH',*resp.registers))
lla3 = float("%.3f" % lla3[0])
f = open('/var/www/html/openWB/ramdisk/lla3', 'w')
f.write(str(lla3))
f.close()
resp = client.read_input_registers(0x0C,2, unit=sdm3id)
ll = struct.unpack('>f',struct.pack('>HH',*resp.registers))
wl3 = int(ll[0])
resp = client.read_input_registers(0x0156,2, unit=sdm3id)
llwh = struct.unpack('>f',struct.pack('>HH',*resp.registers))
llwh3 = float("%.3f" % llwh[0])

llwh = llwh1 + llwh2 + llwh3
f = open('/var/www/html/openWB/ramdisk/llkwh', 'w')
f.write(str(llwh))
f.close()

ll = wl1 + wl2 + wl3
f = open('/var/www/html/openWB/ramdisk/llaktuell', 'w')
f.write(str(ll))
f.close()
