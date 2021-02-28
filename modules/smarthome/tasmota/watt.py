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
import urllib.request
named_tuple = time.localtime() # getstruct_time
time_string = time.strftime("%m/%d/%Y, %H:%M:%S tasmota watty.py", named_tuple)
devicenumber=str(sys.argv[1])
ipadr=str(sys.argv[2])
uberschuss=int(sys.argv[3])
answer = json.loads(str(urllib.request.urlopen("http://"+str(ipadr)+"/cm?cmnd=Status%208", timeout=3).read().decode("utf-8")))
aktpower = int(answer['StatusSNS']['ENERGY']['Power'])
#if ( int(answer['StatusSNS']['ENERGY']['Voltage']) > 50 ):
if aktpower > 50:
   relais=1
else:
   relais=0
powerc = 0
answer = '{"power":' + str(aktpower) + ',"powerc":' + str(powerc) + ',"on":' + str(relais) + '} '
f1 = open('/var/www/html/openWB/ramdisk/smarthome_device_ret' + str(devicenumber), 'w')
json.dump(answer,f1)
f1.close()
