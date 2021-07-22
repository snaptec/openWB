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
sdmid = int(sys.argv[2])
sdm2id = int(sys.argv[3])

client = ModbusSerialClient(method = "rtu", port=seradd, baudrate=9600, stopbits=1, bytesize=8, timeout=1)

# rq = client.read_holding_registers(0,8,unit=5)
# print(rq.registers)
resp = client.read_input_registers(0x00,2, unit=sdmid)
print(struct.unpack('>f',struct.pack('>HH',*resp.registers)))
resp = client.read_input_registers(0x06,2, unit=sdmid)
print(struct.unpack('>f',struct.pack('>HH',*resp.registers)))
resp = client.read_input_registers(0x0C,2, unit=sdmid)
print(struct.unpack('>f',struct.pack('>HH',*resp.registers)))
resp = client.read_input_registers(0x1E,2, unit=sdmid)
print(struct.unpack('>f',struct.pack('>HH',*resp.registers)))
resp = client.read_input_registers(0x0156,2, unit=sdmid)
print(struct.unpack('>f',struct.pack('>HH',*resp.registers)))
time.sleep(0.3)
resp = client.read_input_registers(0x00,2, unit=sdm2id)
print(struct.unpack('>f',struct.pack('>HH',*resp.registers)))
resp = client.read_input_registers(0x06,2, unit=sdm2id)
print(struct.unpack('>f',struct.pack('>HH',*resp.registers)))
resp = client.read_input_registers(0x0C,2, unit=sdm2id)
print(struct.unpack('>f',struct.pack('>HH',*resp.registers)))
resp = client.read_input_registers(0x1E,2, unit=sdm2id)
print(struct.unpack('>f',struct.pack('>HH',*resp.registers)))
resp = client.read_input_registers(0x0156,2, unit=sdm2id)
print(struct.unpack('>f',struct.pack('>HH',*resp.registers)))
