#!/usr/bin/python3
import sys
import os
import time
import json
import getopt
import socket
import struct
import codecs
from pymodbus.client.sync import ModbusTcpClient
#from pymodbus.client.sync import ModbusTcpClient
named_tuple = time.localtime() # getstruct_time
time_string = time.strftime("%m/%d/%Y, %H:%M:%S acthor on.py", named_tuple)
devicenumber=str(sys.argv[1])
ipadr=str(sys.argv[2])
uberschuss=int(sys.argv[3])
# standard
# lesen
# own log
file_string= '/var/www/html/openWB/ramdisk/smarthome_device_' + str(devicenumber) + '_acthor.log'
file_stringpv= '/var/www/html/openWB/ramdisk/smarthome_device_' + str(devicenumber) + '_pv'
file_stringcount= '/var/www/html/openWB/ramdisk/smarthome_device_' + str(devicenumber) + '_count'
file_stringcount5= '/var/www/html/openWB/ramdisk/smarthome_device_' + str(devicenumber) + '_count5'
file_stringold= '/var/www/html/openWB/ramdisk/smarthome_device_' + str(devicenumber) + '_oldpower'
if os.path.isfile(file_string):
   f = open( file_string , 'a')
else:
   f = open( file_string , 'w')
print ('%s devicenr %s ipadr %s ueberschuss %6d try to connect (modbus)' % (time_string,devicenumber,ipadr,uberschuss),file=f)
client = ModbusTcpClient(ipadr, port=502)
start = 1000
resp=client.read_holding_registers(start,10,unit=1)
#start = 3524 
#resp=client.read_input_registers(start,10,unit=1)
value1 = resp.registers[0]
all = format(value1, '04x')
aktpower= int(struct.unpack('>h',codecs.decode(all, 'hex') )[0])
value1 = resp.registers[3]
all = format(value1, '04x')
status= int(struct.unpack('>h',codecs.decode(all, 'hex') )[0])
print ('%s devicenr %s ipadr %s Akt Leistung  %6d Status %2d' % (time_string,devicenumber,ipadr,aktpower,status),file=f)
f.close()
f = open( file_stringpv , 'w')
f.write(str(1))
f.close()
count1 = 999
f = open( file_stringcount , 'w')
f.write(str(count1))
f.close()
count5= 999
f = open( file_stringcount5 , 'w')
f.write(str(count5))
f.close()   
f = open( file_stringold , 'w')
f.write(str(1000))
f.close()
