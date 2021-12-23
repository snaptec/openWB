#!/usr/bin/python
import sys
# import os
# import time
# import getopt
# import socket
# import ConfigParser
import struct
# import binascii
from pymodbus.client.sync import ModbusTcpClient

ipaddress = str(sys.argv[1])
zweiterspeicher = int(sys.argv[2])
storage2power = 0

client = ModbusTcpClient(ipaddress, port=502)

rr = client.read_holding_registers(62836, 2, unit=1)
raw = struct.pack('>HH', rr.getRegister(1), rr.getRegister(0))
storagepower = int(struct.unpack('>f', raw)[0])
if zweiterspeicher == 1:
    rr = client.read_holding_registers(62836, 2, unit=2)
    raw = struct.pack('>HH', rr.getRegister(1), rr.getRegister(0))
    storage2power = int(struct.unpack('>f', raw)[0])
final=storagepower+storage2power
f = open('/var/www/html/openWB/ramdisk/speicherleistung', 'w')
f.write(str(final))
f.close()

rr = client.read_holding_registers(62852, 2, unit=1)
raw = struct.pack('>HH', rr.getRegister(1), rr.getRegister(0))
soc = int(struct.unpack('>f', raw)[0])
if zweiterspeicher == 1:
    rr = client.read_holding_registers(62852, 2, unit=2)
    raw = struct.pack('>HH', rr.getRegister(1), rr.getRegister(0))
    soc2 = int(struct.unpack('>f', raw)[0])
    fsoc=(soc+soc2)/2
else:
    fsoc=soc
f = open('/var/www/html/openWB/ramdisk/speichersoc', 'w')
f.write(str(fsoc))
f.close()
