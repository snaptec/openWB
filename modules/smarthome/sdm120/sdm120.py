#!/usr/bin/python3
import sys
import os
import time
import getopt
import socket
import struct
import binascii
import json
devicenumber = str(sys.argv[1])
seradd = str(sys.argv[2])
sdmid = int(sys.argv[3])
port = int(sys.argv[4])

from pymodbus.client.sync import ModbusTcpClient

client = ModbusTcpClient(seradd, port=port)

#KWH Total Import
resp = client.read_input_registers(0x0048,2, unit=sdmid)
vwh = struct.unpack('>f',struct.pack('>HH',*resp.registers))
vwh2 = float("%.3f" % vwh[0]) * int(1000)
vwh3 = str(vwh2)

#Aktueller Verbrauch
resp = client.read_input_registers(0x000C,2, unit=sdmid)
watti = struct.unpack('>f',struct.pack('>HH',*resp.registers))
watt = int(watti[0])

answer = '{"power":' + str(watt) + ',"powerc":' + str(vwh3) + '} '
f1 = open('/var/www/html/openWB/ramdisk/smarthome_device_ret' + str(devicenumber), 'w')
json.dump(answer,f1)
f1.close()
