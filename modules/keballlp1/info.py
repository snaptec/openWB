#!/usr/bin/python3
import sys
import os
import time
import json
import getopt
import socket
import struct
import codecs
import binascii
from pymodbus.client.sync import ModbusTcpClient
from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadDecoder
named_tuple = time.localtime() # getstruct_time
time_string = time.strftime("%m/%d/%Y, %H:%M:%S keba info.py", named_tuple)
lpnumber=int(sys.argv[1])
ipaddress=str(sys.argv[2])
client = ModbusTcpClient(ipaddress, port=502)
# total energy 1036
resp= client.read_holding_registers(1036,2,unit=255)
if (lpnumber ==1):
    f = open('/var/www/html/openWB/ramdisk/llkwh', 'w')
else:
    f = open('/var/www/html/openWB/ramdisk/llkwhs1', 'w')
decoder = BinaryPayloadDecoder.fromRegisters(resp.registers,byteorder=Endian.Big,wordorder=Endian.Big)
final2 = float( decoder.decode_32bit_uint()) / 10000
final3 = "%.3f" % final2
f.write(str(final3))
f.close()
# active power 1020
resp= client.read_holding_registers(1020,2,unit=255)
if (lpnumber ==1):
    f = open('/var/www/html/openWB/ramdisk/llaktuell', 'w')
else:
    f = open('/var/www/html/openWB/ramdisk/llaktuells1', 'w')
decoder = BinaryPayloadDecoder.fromRegisters(resp.registers,byteorder=Endian.Big,wordorder=Endian.Big)
final2 = float( decoder.decode_32bit_uint()) / 1000
final3 = "%.f" % final2
f.write(str(final3))
f.close()
# voltage l1 1040
resp= client.read_holding_registers(1040,2,unit=255)
if (lpnumber ==1):
    f = open('/var/www/html/openWB/ramdisk/llv1', 'w')
else:
    f = open('/var/www/html/openWB/ramdisk/llvs11', 'w')
decoder = BinaryPayloadDecoder.fromRegisters(resp.registers,byteorder=Endian.Big,wordorder=Endian.Big)
final2 = float( decoder.decode_32bit_uint())
final3 = "%.f" % final2
f.write(str(final3))
f.close()
# voltage l2 1042
resp= client.read_holding_registers(1042,2,unit=255)
if (lpnumber ==1):
    f = open('/var/www/html/openWB/ramdisk/llv2', 'w')
else:
    f = open('/var/www/html/openWB/ramdisk/llvs12', 'w')
decoder = BinaryPayloadDecoder.fromRegisters(resp.registers,byteorder=Endian.Big,wordorder=Endian.Big)
final2 = float( decoder.decode_32bit_uint())
final3 = "%.f" % final2
f.write(str(final3))
f.close()
# voltage l3 1044
resp= client.read_holding_registers(1044,2,unit=255)
if (lpnumber ==1):
    f = open('/var/www/html/openWB/ramdisk/llv3', 'w')
else:
    f = open('/var/www/html/openWB/ramdisk/llvs13', 'w')
decoder = BinaryPayloadDecoder.fromRegisters(resp.registers,byteorder=Endian.Big,wordorder=Endian.Big)
final2 = float( decoder.decode_32bit_uint())
final3 = "%.f" % final2
f.write(str(final3))
f.close()
# amp l1 1008
resp= client.read_holding_registers(1008,2,unit=255)
if (lpnumber ==1):
    f = open('/var/www/html/openWB/ramdisk/lla1', 'w')
else:
    f = open('/var/www/html/openWB/ramdisk/llas11', 'w')
decoder = BinaryPayloadDecoder.fromRegisters(resp.registers,byteorder=Endian.Big,wordorder=Endian.Big)
final2 = float( decoder.decode_32bit_uint()) / 1000
final3 = "%.2f" % final2
f.write(str(final3))
f.close()
# amp l2 1010
resp= client.read_holding_registers(1010,2,unit=255)
if (lpnumber ==1):
    f = open('/var/www/html/openWB/ramdisk/lla2', 'w')
else:
    f = open('/var/www/html/openWB/ramdisk/llas12', 'w')
decoder = BinaryPayloadDecoder.fromRegisters(resp.registers,byteorder=Endian.Big,wordorder=Endian.Big)
final2 = float( decoder.decode_32bit_uint()) / 1000
final3 = "%.2f" % final2
f.write(str(final3))
f.close()
# amp l3 1012
resp= client.read_holding_registers(1012,2,unit=255)
if (lpnumber ==1):
    f = open('/var/www/html/openWB/ramdisk/lla3', 'w')
else:
    f = open('/var/www/html/openWB/ramdisk/llas13', 'w')
decoder = BinaryPayloadDecoder.fromRegisters(resp.registers,byteorder=Endian.Big,wordorder=Endian.Big)
final2 = float( decoder.decode_32bit_uint()) / 1000
final3 = "%.2f" % final2
f.write(str(final3))
f.close()
# charging state 1000
resp= client.read_holding_registers(1000,2,unit=255)
if (lpnumber ==1):
    f = open('/var/www/html/openWB/ramdisk/chargestat', 'w')
else:
    f = open('/var/www/html/openWB/ramdisk/chargestats1', 'w')
decoder = BinaryPayloadDecoder.fromRegisters(resp.registers,byteorder=Endian.Big,wordorder=Endian.Big)
final2 = float( decoder.decode_32bit_uint())
final3 = "%.f" % final2
if (final3 == "3"):
    f.write(str(1))
else:
    f.write(str(0))
f.close()
# cabel state 1004
resp= client.read_holding_registers(1004,2,unit=255)
if (lpnumber ==1):
    f = open('/var/www/html/openWB/ramdisk/plugstat', 'w')
else:
    f = open('/var/www/html/openWB/ramdisk/plugstats1', 'w')
decoder = BinaryPayloadDecoder.fromRegisters(resp.registers,byteorder=Endian.Big,wordorder=Endian.Big)
final2 = float( decoder.decode_32bit_uint())
final3 = "%.f" % final2
if (final3 == "7"):
    f.write(str(1))
else:
    f.write(str(0))
f.close()
# maxcurr state 1100
resp= client.read_holding_registers(1100,2,unit=255)
if (lpnumber ==1):
    f = open('/var/www/html/openWB/ramdisk/kebamaxlp1', 'w')
else:
    f = open('/var/www/html/openWB/ramdisk/kebamaxlp2', 'w')
decoder = BinaryPayloadDecoder.fromRegisters(resp.registers,byteorder=Endian.Big,wordorder=Endian.Big)
final2 = float( decoder.decode_32bit_uint()) / 1000
final3 = "%.f" % final2
f.write(str(final3))
f.close()
