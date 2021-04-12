#!/usr/bin/python
import sys
import os
import time
import getopt
import socket
import ConfigParser
import struct
import binascii
from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadDecoder
ipaddress = str(sys.argv[1])
from pymodbus.client.sync import ModbusTcpClient
client = ModbusTcpClient(ipaddress, port=502)
connection = client.connect()


#Studer Battery Power
request = client.read_input_registers(6,2,unit=60)
if request.isError():
    # handle error, log?
    print('Modbus Error:', request)
else:
    result = request.registers
    #print(result)
decoder = BinaryPayloadDecoder.fromRegisters(result, byteorder=Endian.Big)
#bw = (decoder.decode_32bit_float()) * -1 # type: float
bw = decoder.decode_32bit_float() # type: float
f = open('/var/www/html/openWB/ramdisk/speicherleistung', 'w')
f.write(str(bw))
f.close()


#Studer SOC
request = client.read_input_registers(4,2,unit=60)
if request.isError():
    # handle error, log?
    print('Modbus Error:', request)
else:
    result = request.registers
    #print(result)
decoder = BinaryPayloadDecoder.fromRegisters(result, byteorder=Endian.Big)
bs= decoder.decode_32bit_float()  # type: float
f = open('/var/www/html/openWB/ramdisk/speichersoc', 'w')
f.write(str(bs))
f.close()

client.close()

