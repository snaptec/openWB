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
from urllib.parse import urlparse
named_tuple = time.localtime() # getstruct_time
time_string = time.strftime("%m/%d/%Y, %H:%M:%S http watty.py", named_tuple)
devicenumber=str(sys.argv[1])
uberschuss=int(sys.argv[3])
url=str(sys.argv[4])
if not urlparse(url).scheme:
   url = 'http://' + url
if uberschuss < 0:
   uberschuss = 0
urlrep= url.replace("<openwb-ueberschuss>", str(uberschuss))
file_string= '/var/www/html/openWB/ramdisk/smarthome_device_' + str(devicenumber) + '_http.log'
if os.path.isfile(file_string):
   f = open( file_string , 'a')
else:
   f = open( file_string , 'w')
print ('%s devicenr %s orig url %s replaced url %s' % (time_string,devicenumber,url,urlrep),file=f)
f.close()
aktpower = int(urllib.request.urlopen(urlrep, timeout=5).read().decode("utf-8"))
if aktpower > 50:
    relais = 1
else:
    relais = 0
powerc = 0
answer = '{"power":' + str(aktpower) + ',"powerc":' + str(powerc) + ',"on":' + str(relais) + '} '
f1 = open('/var/www/html/openWB/ramdisk/smarthome_device_ret' + str(devicenumber), 'w')
json.dump(answer,f1)
f1.close() 