#!/usr/bin/python3
import sys
import os
import time
import getopt
import socket
import ConfigParser
import struct
import binascii
ip = str(sys.argv[2])
from pymodbus.client.sync import ModbusTcpClient
lla = int(sys.argv[1])
client = ModbusTcpClient(ip, port=502)
#EnableSet
if lla < 6:
 client.write_coil(400,False,unit=180)
else:
 client.write_coil(400, True, unit=180)
if lla < 6:
 lla = 6
rq = client.write_registers(300, lla, unit=180)
