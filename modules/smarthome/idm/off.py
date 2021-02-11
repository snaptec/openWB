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
from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadDecoder
from pymodbus.payload import BinaryPayloadBuilder
from pymodbus.client.sync import ModbusTcpClient

named_tuple = time.localtime() # getstruct_time
time_string = time.strftime("%m/%d/%Y, %H:%M:%S idm off.py", named_tuple)
devicenumber=str(sys.argv[1])
ipadr=str(sys.argv[2])
uberschuss=int(sys.argv[3])
# standard
file_string= '/var/www/html/openWB/ramdisk/smarthome_device_' + str(devicenumber) + '_idm.log'
file_stringpv= '/var/www/html/openWB/ramdisk/smarthome_device_' + str(devicenumber) + '_pv'
file_stringcount= '/var/www/html/openWB/ramdisk/smarthome_device_' + str(devicenumber) + '_count'
if os.path.isfile(file_string):
   f = open( file_string , 'a')
else:
   f = open( file_string , 'w')
print ('%s devicenr %s ipadr %s ueberschuss %6d try to connect (modbus)' % (time_string,devicenumber,ipadr,uberschuss),file=f)

client = ModbusTcpClient(ipadr, port=502)
#start = 3524 
start = 4122
rr=client.read_input_registers(start,2,unit=1)
raw = struct.pack('>HH', rr.getRegister(1), rr.getRegister(0))
lkw= float(struct.unpack('>f', raw)[0])
aktpower = int(lkw*1000)
print ('%s devicenr %s ipadr %s Akt Leistung  %6d' % (time_string,devicenumber,ipadr,aktpower),file=f)
f.close()
pvmodus = 0
if os.path.isfile(file_stringpv):
   f = open( file_stringpv , 'r')
   pvmodus =int(f.read())
   f.close()
#wenn vorher pvmodus an, dann watt.py signaliseren einmalig 0 ueberschuss zu schicken
if pvmodus == 1:
   pvmodus = 99
f = open( file_stringpv , 'w')
f.write(str(pvmodus))
f.close()
count1 = 999
f = open( file_stringcount , 'w')
f.write(str(count1))
f.close()
 