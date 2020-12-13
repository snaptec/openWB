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
time_string = time.strftime("%m/%d/%Y, %H:%M:%S http on.py", named_tuple)
devicenumber=str(sys.argv[1])
uberschuss=int(sys.argv[3])
url=str(sys.argv[4])
if not urlparse(url).scheme:
   url = 'http://' + url
file_string= '/var/www/html/openWB/ramdisk/smarthome_device_' + str(devicenumber) + '_http.log'
if os.path.isfile(file_string):
   f = open( file_string , 'a')
else:
   f = open( file_string , 'w')
print ('%s devicenr %s url %s)' % (time_string,devicenumber,url),file=f)
f.close()
urllib.request.urlopen(url, timeout=5)