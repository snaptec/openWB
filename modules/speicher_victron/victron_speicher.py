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

# Battery Voltage
# resp= client.read_holding_registers(840,1,unit=100)
# decoder = BinaryPayloadDecoder.fromRegisters(resp.registers,byteorder=Endian.Big,wordorder=Endian.Big)
# bv = str(decoder.decode_16bit_uint())
# bv = float(bv) / 10
# f = open('/var/www/html/openWB/ramdisk/???', 'w')
# f.write(str(watt))
# f.close()
# print "Batteriespannung aktuell:"
# print bv

# Battery ampere
# resp= client.read_holding_registers(841,1,unit=100)
# decoder = BinaryPayloadDecoder.fromRegisters(resp.registers,byteorder=Endian.Big,wordorder=Endian.Big)
# ba = str(decoder.decode_16bit_int())
# ba = float(ba) / 10
# f = open('/var/www/html/openWB/ramdisk/???', 'w')
# f.write(str(a3))
# f.close()
# print "Batterie Ampere +/- aktuell:"
# print ba

# Battery watt
resp= client.read_holding_registers(842,1,unit=100)
decoder = BinaryPayloadDecoder.fromRegisters(resp.registers,byteorder=Endian.Big,wordorder=Endian.Big)
bw = str(decoder.decode_16bit_int())
f = open('/var/www/html/openWB/ramdisk/speicherleistung', 'w')
f.write(str(bw))
f.close()
# print "Batterie Wirkleistung +/- aktuell:"
# print bw

# Battery SOC
resp= client.read_holding_registers(843,1,unit=100)
decoder = BinaryPayloadDecoder.fromRegisters(resp.registers,byteorder=Endian.Big,wordorder=Endian.Big)
bs = str(decoder.decode_16bit_uint())
f = open('/var/www/html/openWB/ramdisk/speichersoc', 'w')
f.write(str(bs))
f.close()
# print "Batterie SOC aktuell:"
# print bs

client.close()
