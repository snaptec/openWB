#!/usr/bin/python
import sys
import os
import time
import getopt
import socket
import ConfigParser
import struct
import binascii
from pymodbus.payload import BinaryPayloadDecoder
from pymodbus.constants import Endian

seradd = str(sys.argv[1])
if "dev" in seradd:
    from pymodbus.client.sync import ModbusSerialClient
    client = ModbusSerialClient(method = "rtu", port=seradd, baudrate=9600,
                                        stopbits=1, bytesize=8, timeout=1)
else:
    from pymodbus.client.sync import ModbusTcpClient
    client = ModbusTcpClient('192.168.193.31', port=8899)

sdmid = int(85)
time.sleep(0.1)
resp = client.read_holding_registers(0x0008,2, unit=sdmid)
decoder = BinaryPayloadDecoder.fromRegisters(resp.registers,byteorder=Endian.Big,wordorder=Endian.Big)
w2 = str(decoder.decode_16bit_int())
f = open('/var/www/html/openWB/ramdisk/wattbezug', 'w')
f.write(str(w2))
f.close()
time.sleep(0.1)
resp = client.read_holding_registers(0x0009,4, unit=sdmid)
decoder = BinaryPayloadDecoder.fromRegisters(resp.registers,byteorder=Endian.Big,wordorder=Endian.Big)
w2 = int(decoder.decode_32bit_int())
iwh = w2 * 10
f = open('/var/www/html/openWB/ramdisk/bezugkwh', 'w')
f.write(str(iwh))
f.close()

time.sleep(0.1)
resp = client.read_holding_registers(0x000B,4, unit=sdmid)
decoder = BinaryPayloadDecoder.fromRegisters(resp.registers,byteorder=Endian.Big,wordorder=Endian.Big)
w2 = int(decoder.decode_32bit_int())
ewh = w2 * 10
f = open('/var/www/html/openWB/ramdisk/einspeisungkwh', 'w')
f.write(str(ewh))
f.close()


