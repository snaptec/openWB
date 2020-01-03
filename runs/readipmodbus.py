#!/usr/bin/python3
import sys
import os
import time
import getopt
import socket
import struct
import binascii


ipadd = str(sys.argv[1])
from pymodbus.client.sync import ModbusTcpClient
client = ModbusTcpClient(ipadd, port=8899)


#rq = client.read_holding_registers(0,8,unit=5)
#print(rq.registers)
modbusid = int(sys.argv[2])
readreg = int(sys.argv[3])
reganzahl = int(sys.argv[4])

rq = client.read_holding_registers(readreg,reganzahl,unit=modbusid)
print(rq.registers[0])














