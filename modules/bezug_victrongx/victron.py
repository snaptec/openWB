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
mid = int(sys.argv[2])
from pymodbus.client.sync import ModbusTcpClient
client = ModbusTcpClient(ipaddress, port=502)
connection = client.connect()


#grid power
resp= client.read_holding_registers(2600,2,unit=mid)
decoder = BinaryPayloadDecoder.fromRegisters(resp.registers,byteorder=Endian.Big,wordorder=Endian.Little)
w1 = str(decoder.decode_16bit_int())
resp= client.read_holding_registers(2601,2,unit=mid)
decoder = BinaryPayloadDecoder.fromRegisters(resp.registers,byteorder=Endian.Big,wordorder=Endian.Little)
w2 = str(decoder.decode_16bit_int())
resp= client.read_holding_registers(2602,2,unit=mid)
decoder = BinaryPayloadDecoder.fromRegisters(resp.registers,byteorder=Endian.Big,wordorder=Endian.Little)
w3 = str(decoder.decode_16bit_int())
watt = int(w1) + int(w2) + int(w3)
f = open('/var/www/html/openWB/ramdisk/wattbezug', 'w')
f.write(str(watt))
f.close()

#grid ampere
resp= client.read_holding_registers(2617,2,unit=mid)
decoder = BinaryPayloadDecoder.fromRegisters(resp.registers,byteorder=Endian.Big,wordorder=Endian.Little)
a1 = str(decoder.decode_16bit_int())
a1 = float(a1) / 10
resp= client.read_holding_registers(2619,2,unit=mid)
decoder = BinaryPayloadDecoder.fromRegisters(resp.registers,byteorder=Endian.Big,wordorder=Endian.Little)
a2 = str(decoder.decode_16bit_int())
a2 = float(a2) / 10
resp= client.read_holding_registers(2621,2,unit=mid)
decoder = BinaryPayloadDecoder.fromRegisters(resp.registers,byteorder=Endian.Big,wordorder=Endian.Little)
a3 = str(decoder.decode_16bit_int())
a3 = float(a3) / 10
f = open('/var/www/html/openWB/ramdisk/bezuga1', 'w')
f.write(str(a1))
f.close()
f = open('/var/www/html/openWB/ramdisk/bezuga2', 'w')
f.write(str(a2))
f.close()
f = open('/var/www/html/openWB/ramdisk/bezuga3', 'w')
f.write(str(a3))
f.close()

#grid voltage
resp= client.read_holding_registers(2616,2,unit=mid)
decoder = BinaryPayloadDecoder.fromRegisters(resp.registers,byteorder=Endian.Big,wordorder=Endian.Little)
v1 = str(decoder.decode_16bit_uint())
v1 = float(v1) / 10
resp= client.read_holding_registers(2618,2,unit=mid)
decoder = BinaryPayloadDecoder.fromRegisters(resp.registers,byteorder=Endian.Big,wordorder=Endian.Little)
v2 = str(decoder.decode_16bit_uint())
v2 = float(v2) / 10
resp= client.read_holding_registers(2620,2,unit=mid)
decoder = BinaryPayloadDecoder.fromRegisters(resp.registers,byteorder=Endian.Big,wordorder=Endian.Little)
v3 = str(decoder.decode_16bit_uint())
v3 = float(v3) / 10
f = open('/var/www/html/openWB/ramdisk/evuv1', 'w')
f.write(str(v1))
f.close()
f = open('/var/www/html/openWB/ramdisk/evuv2', 'w')
f.write(str(v2))
f.close()
f = open('/var/www/html/openWB/ramdisk/evuv3', 'w')
f.write(str(v3))
f.close()

#grid import
resp= client.read_holding_registers(2622,4,unit=mid)
decoder = BinaryPayloadDecoder.fromRegisters(resp.registers,byteorder=Endian.Big,wordorder=Endian.Little)
wh1 = str(decoder.decode_32bit_uint())
resp= client.read_holding_registers(2624,4,unit=mid)
decoder = BinaryPayloadDecoder.fromRegisters(resp.registers,byteorder=Endian.Big,wordorder=Endian.Little)
wh2 = str(decoder.decode_32bit_uint())
resp= client.read_holding_registers(2626,4,unit=mid)
decoder = BinaryPayloadDecoder.fromRegisters(resp.registers,byteorder=Endian.Big,wordorder=Endian.Little)
wh3 = str(decoder.decode_32bit_uint())

whs = int(wh1) + int(wh2) + int(wh3)
whs = whs * 10
f = open('/var/www/html/openWB/ramdisk/bezugkwh', 'w')
f.write(str(whs))
f.close()

#grid export
resp= client.read_holding_registers(2628,4,unit=mid)
decoder = BinaryPayloadDecoder.fromRegisters(resp.registers,byteorder=Endian.Big,wordorder=Endian.Little)
whe1 = str(decoder.decode_32bit_uint())
resp= client.read_holding_registers(2630,4,unit=mid)
decoder = BinaryPayloadDecoder.fromRegisters(resp.registers,byteorder=Endian.Big,wordorder=Endian.Little)
whe2 = str(decoder.decode_32bit_uint())
resp= client.read_holding_registers(2632,4,unit=mid)
decoder = BinaryPayloadDecoder.fromRegisters(resp.registers,byteorder=Endian.Big,wordorder=Endian.Little)
whe3 = str(decoder.decode_32bit_uint())

whes = int(whe1) + int(whe2) + int(whe3)
whes = whes * 10
f = open('/var/www/html/openWB/ramdisk/einspeisungkwh', 'w')
f.write(str(whes))
f.close()


client.close()

