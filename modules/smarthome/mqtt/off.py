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
named_tuple = time.localtime() # getstruct_time
time_string = time.strftime("%m/%d/%Y, %H:%M:%S mqtt off.py", named_tuple)
devicenumber=str(sys.argv[1])
ipadr=str(sys.argv[2])
uberschuss=int(sys.argv[3])
# standard
file_string= '/var/www/html/openWB/ramdisk/smarthome_device_' + str(devicenumber) + '_mqtt.log'
file_stringpv= '/var/www/html/openWB/ramdisk/smarthome_device_' + str(devicenumber) + '_pv'
if os.path.isfile(file_string):
   f = open( file_string , 'a')
else:
   f = open( file_string , 'w')
print ('%s devicenr %s ipadr %s ueberschuss %6d ' % (time_string,devicenumber,ipadr,uberschuss),file=f)
f.close()
pvmodus = 0
f = open( file_stringpv , 'w')
f.write(str(pvmodus))
f.close()
