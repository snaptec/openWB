#!/usr/bin/python
import sys
import os
import time
import getopt
import socket
import ConfigParser
import struct
import binascii
ipaddress = str(sys.argv[1])
from pymodbus.client.sync import ModbusTcpClient
client = ModbusTcpClient(ipaddress, port=502)

rr = client.read_holding_registers(62836, 2, unit=1)
raw = struct.pack('>HH', rr.getRegister(1), rr.getRegister(0))
storagepower = int(struct.unpack('>f', raw)[0])
f = open('/var/www/html/openWB/ramdisk/speicherleistung', 'w')
f.write(str(storagepower))
f.close()


rr = client.read_holding_registers(62852, 2, unit=1)
raw = struct.pack('>HH', rr.getRegister(1), rr.getRegister(0))
soc = int(struct.unpack('>f', raw)[0])
f = open('/var/www/html/openWB/ramdisk/speichersoc', 'w')
f.write(str(soc))
f.close()




