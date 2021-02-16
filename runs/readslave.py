#!/usr/bin/python3
import sys
import os
import time
import getopt
import socket
import struct
import binascii
from pymodbus.client.sync import ModbusTcpClient

readreg = int(sys.argv[1])
reganzahl = int(sys.argv[2])

client = ModbusTcpClient('192.168.193.16', port=8899)
rq = client.read_holding_registers(readreg,reganzahl,unit=1)
print(rq.registers[0])
