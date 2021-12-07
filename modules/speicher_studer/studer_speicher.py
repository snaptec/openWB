#!/usr/bin/python
import sys
# import os
# import time
# import getopt
# import socket
# import ConfigParser
# import struct
# import binascii
from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadDecoder
from pymodbus.client.sync import ModbusTcpClient

ipaddress = str(sys.argv[1])

client = ModbusTcpClient(ipaddress, port=502)
connection = client.connect()

# Studer Battery Power
request = client.read_input_registers(6, 2, unit=60)
if request.isError():
    # handle error, log?
    print('Modbus Error:', request)
else:
    result = request.registers
decoder = BinaryPayloadDecoder.fromRegisters(result, byteorder=Endian.Big)
bw = decoder.decode_32bit_float()  # type: float
f = open('/var/www/html/openWB/ramdisk/speicherleistung', 'w')
f.write(str(bw))
f.close()

# Studer SOC
request = client.read_input_registers(4, 2, unit=60)
if request.isError():
    # handle error, log?
    print('Modbus Error:', request)
else:
    result = request.registers
decoder = BinaryPayloadDecoder.fromRegisters(result, byteorder=Endian.Big)
bs = decoder.decode_32bit_float()  # type: float
f = open('/var/www/html/openWB/ramdisk/speichersoc', 'w')
f.write(str(bs))
f.close()

# Studer charged Energy
request = client.read_input_registers(14, 2, unit=60)
if request.isError():
    # handle error, log?
    print('Modbus Error:', request)
else:
    result = request.registers
decoder = BinaryPayloadDecoder.fromRegisters(result, byteorder=Endian.Big)
bc = decoder.decode_32bit_float()  # type: float
f = open('/var/www/html/openWB/ramdisk/speicherikwh', 'w')
f.write(str(bc*48))
f.close()

# Studer discharged Energy
request = client.read_input_registers(16, 2, unit=60)
if request.isError():
    # handle error, log?
    print('Modbus Error:', request)
else:
    result = request.registers
decoder = BinaryPayloadDecoder.fromRegisters(result, byteorder=Endian.Big)
bd = decoder.decode_32bit_float()  # type: float
f = open('/var/www/html/openWB/ramdisk/speicherekwh', 'w')
f.write(str(bd*48))
f.close()

client.close()
