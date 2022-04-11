#!/usr/bin/python
import sys
import os
import time
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
socketv = struct.unpack('>f',struct.pack('>HH',*resp.registers))
socketv = float("%.1f" % socketv[0])
f = open('/var/www/html/openWB/ramdisk/socketv', 'w')
f.write(str(socketv))
f.close()

time.sleep(0.1)
resp = client.read_input_registers(0x06,2, unit=sdmid)
socketa = struct.unpack('>f',struct.pack('>HH',*resp.registers))
socketa = float("%.3f" % socketa[0])
f = open('/var/www/html/openWB/ramdisk/socketa', 'w')
f.write(str(socketa))
f.close()

time.sleep(0.1)
resp = client.read_input_registers(0x0C,2, unit=sdmid)
socketp = struct.unpack('>f',struct.pack('>HH',*resp.registers))
socketp = int(socketp[0])
f = open('/var/www/html/openWB/ramdisk/socketp', 'w')
f.write(str(socketp))
f.close()

time.sleep(0.1)
resp = client.read_input_registers(0x1E,2, unit=sdmid)
socketpf = struct.unpack('>f',struct.pack('>HH',*resp.registers))
socketpf = float("%.3f" % socketpf[0])
f = open('/var/www/html/openWB/ramdisk/socketpf', 'w')
f.write(str(socketpf))
f.close()

time.sleep(0.15)
resp = client.read_input_registers(0x0156,2, unit=sdmid)
socketkwh = struct.unpack('>f',struct.pack('>HH',*resp.registers))
socketkwh = float("%.3f" % socketkwh[0])
f = open('/var/www/html/openWB/ramdisk/socketkwh', 'w')
f.write(str(socketkwh))
f.close()

if not os.path.isfile("/var/www/html/openWB/ramdisk/socketSerial"):
    print("Trying to read socket meter serial number once from meter at address " + str(seradd) + ", ID " + str(sdmid))
    try:
        time.sleep(0.2)
        resp = client.read_holding_registers(0xFC00,2, unit=sdmid)
        sn = struct.unpack('>I',struct.pack('>HH',*resp.registers))[0]
        f = open('/var/www/html/openWB/ramdisk/socketSerial', 'w')
        f.write(str(sn))
        f.close()
        print("Socket meter serial number from meter at address " + str(seradd) + ", ID " + str(sdmid) + " is " + str(sn))
    except:
        print("Socket meter serial number of meter at address " + str(seradd) + ", ID " + str(sdmid) + " is not available")
        f = open('/var/www/html/openWB/ramdisk/socketSerial', 'w')
        f.write("0")
        f.close()
