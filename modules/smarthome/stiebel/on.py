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
named_tuple = time.localtime() # getstruct_time
time_string = time.strftime("%m/%d/%Y, %H:%M:%S stiebel on.py", named_tuple)
devicenumber=str(sys.argv[1])
ipadr=str(sys.argv[2])
uberschuss=int(sys.argv[3])
# standard
# lesen
# own log
file_string= '/var/www/html/openWB/ramdisk/smarthome_device_' + str(devicenumber) + '_stiebel.log'
file_stringpv= '/var/www/html/openWB/ramdisk/smarthome_device_' + str(devicenumber) + '_pv'
if os.path.isfile(file_string):
   f = open( file_string , 'a')
else:
   f = open( file_string , 'w')
print ('%s devicenr %s ipadr %s ueberschuss %6d try to connect (modbus)' % (time_string,devicenumber,ipadr,uberschuss),file=f)
client = ModbusTcpClient(ipadr, port=502)
# activate switch one (manual 4002)
rq = client.write_register(4001, 1, unit=1)
print ('%s devicenr %s ipadr %s ' % (time_string,devicenumber,ipadr),file=f)
f.close()
f = open( file_stringpv , 'w')
f.write(str(1))
f.close()