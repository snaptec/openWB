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
try:
    urlc=str(sys.argv[5])
except:
    urlc = "none"
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
print ('%s devicenr %s orig url %s replaced url %s urlc %s' % (time_string,devicenumber,url,urlrep,urlc),file=f)
f.close()
aktpowerfl = float(urllib.request.urlopen(urlrep, timeout=5).read().decode("utf-8"))
aktpower = int(aktpowerfl)
if aktpower > 50:
    relais = 1
else:
    relais = 0
if len(urlc) < 6:
    powerc = 0
else:
    if not urlparse(urlc).scheme:
        urlc = 'http://' + urlc
    powercfl = float(urllib.request.urlopen(urlc, timeout=5).read().decode("utf-8"))
    powerc = int(powercfl)
answer = '{"power":' + str(aktpower) + ',"powerc":' + str(powerc) + ',"on":' + str(relais) + '} '
f1 = open('/var/www/html/openWB/ramdisk/smarthome_device_ret' + str(devicenumber), 'w')
json.dump(answer,f1)
f1.close()
