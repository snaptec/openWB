#!/usr/bin/python3
import sys
import os
import time
import json
# import getopt
# import socket
# import struct
# import codecs
# import binascii
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
powerc = str(final3)
f.write(powerc)
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
power = str(final3)
f.write(power)
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
v1 = str(final3)
f.write(v1)
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
v2 = str(final3)
f.write(v2)
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
v3 = str(final3)
f.write(v3)
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
a1= str(final3)
f.write(a1)
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
a2= str(final3)
f.write(a2)
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
a3= str(final3)
f.write(a3)
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
    chargestat = 1
else:
    chargestat = 0
f.write(str(chargestat))
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
    plugstat = 1
else:
    plugstat = 0
f.write(str(plugstat))
f.close()

# maxcurr 1100
resp= client.read_holding_registers(1100,2,unit=255)
decoder = BinaryPayloadDecoder.fromRegisters(resp.registers,byteorder=Endian.Big,wordorder=Endian.Big)
final2 = float( decoder.decode_32bit_uint()) / 1000
maxcur = "%.f" % final2

# max supported curr 1110
resp= client.read_holding_registers(1110,2,unit=255)
decoder = BinaryPayloadDecoder.fromRegisters(resp.registers,byteorder=Endian.Big,wordorder=Endian.Big)
final2 = float( decoder.decode_32bit_uint()) / 1000
supcur = "%.f" % final2

# hwinfo 1016
resp= client.read_holding_registers(1016,2,unit=255)
decoder = BinaryPayloadDecoder.fromRegisters(resp.registers,byteorder=Endian.Big,wordorder=Endian.Big)
final2 = float( decoder.decode_32bit_uint())
hwinfo= "%.f" % final2

# error info 1006
resp= client.read_holding_registers(1006,2,unit=255)
decoder = BinaryPayloadDecoder.fromRegisters(resp.registers,byteorder=Endian.Big,wordorder=Endian.Big)
final2 = float( decoder.decode_32bit_uint())
errinfo= "%8X" % int(final2)

# rfid info 1500
resp= client.read_holding_registers(1500,2,unit=255)
decoder = BinaryPayloadDecoder.fromRegisters(resp.registers,byteorder=Endian.Big,wordorder=Endian.Big)
final2 = float( decoder.decode_32bit_uint())
rfidinfo= "%08X" % int(final2)
rfidinfo = '00' + rfidinfo
#rfid simulieren
#if (lpnumber ==1):
#    file_stringtr= '/var/www/html/openWB/ramdisk/kebalp1r'
#else:
#    file_stringtr= '/var/www/html/openWB/ramdisk/kebalp2r'
#if os.path.isfile(file_stringtr):
#    f = open( file_stringtr , 'r')
#    rfidtr=int(f.read())
#    f.close()
#    if rfidtr == 1:
#        rfidinfo = '0004A376A2'
#    if rfidtr == 2:
#        rfidinfo = '0004A2DAA2'
#    if rfidtr == 3:
#        rfidinfo = '000992DAA2'
#rfid simulations end
# firmware version
resp= client.read_holding_registers(1018,2,unit=255)
decoder = BinaryPayloadDecoder.fromRegisters(resp.registers,byteorder=Endian.Big,wordorder=Endian.Big)
final2 = float( decoder.decode_32bit_uint())
firminfo= "%08X" % int(final2)

answer = '{"maxcur":' + str(maxcur) + ',"supcur":' + str(supcur) + ',"hwinfo":' + str(hwinfo) + ',"Error":' + str(errinfo) + ',"plugstat":' + str(plugstat) + ',"chargestat":' + str(chargestat) +  ',"rfid":' + str(rfidinfo)  +  ',"firmware":' + str(firminfo)  +  ',"powerc":' + powerc + ',"power":' + power + ',"V1":' + v1 + ',"V2":' + v2 + ',"V3":' + v3 + ',"A1":' + a1 + ',"A2":' + a2 + ',"A3":' + a3 +'} '
if (lpnumber ==1):
    f = open('/var/www/html/openWB/ramdisk/kebainfolp1', 'w')
else:
    f = open('/var/www/html/openWB/ramdisk/kebainfolp2','w')
json.dump(answer,f)
f.close()
if (lpnumber ==1):
    file_string= '/var/www/html/openWB/ramdisk/kebalp1rfid'
else:
    file_string= '/var/www/html/openWB/ramdisk/kebalp2rfid'
rfidold=rfidinfo
if os.path.isfile(file_string):
    f = open( file_string , 'r')
    rfidold=str(f.read())
    f.close()
    if (rfidold != rfidinfo) and (rfidinfo != '0000000000'):
        f = open( '/var/www/html/openWB/ramdisk/readtag','w')
        f.write(str(rfidinfo))
        f.close()
f = open( file_string , 'w')
f.write(str(rfidinfo))
f.close()
