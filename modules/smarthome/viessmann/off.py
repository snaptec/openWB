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
time_string = time.strftime("%m/%d/%Y, %H:%M:%S viessmann off.py", named_tuple)
devicenumber=str(sys.argv[1])
ipadr=str(sys.argv[2])
uberschuss=int(sys.argv[3])
# standard
#Anzeige und Einstellung der Komfortfunktion "Einmalige Warmwasserbereitung"
#außerhalb des Zeitprogrammes:
#0: "Einmalige Warmwasserbereitung" AUS
#1: "Einmalige Warmwasserbereitung" EIN
#Für die "Einmalige Warmwasserbereitung" wird der Warmwassertemperatur-Sollwert 2 genutzt.
#CO-17
#coiss read write bolean
#register start 00000
#
file_string= '/var/www/html/openWB/ramdisk/smarthome_device_' + str(devicenumber) + '_viessmann.log'
file_stringpv= '/var/www/html/openWB/ramdisk/smarthome_device_' + str(devicenumber) + '_pv'
if os.path.isfile(file_string):
   f = open( file_string , 'a')
else:
   f = open( file_string , 'w')
print ('%s devicenr %s ipadr %s ueberschuss %6d try to connect (modbus)' % (time_string,devicenumber,ipadr,uberschuss),file=f)
client = ModbusTcpClient(ipadr, port=502)
rq = client.write_coil(17, 0)
print ('%s devicenr %s ipadr %s Einmalige Warmwasseraufbereitung deaktiviert CO-17 = 0 ' % (time_string,devicenumber,ipadr),file=f)
f.close()
pvmodus = 0
f = open( file_stringpv , 'w')
f.write(str(pvmodus))
f.close()
