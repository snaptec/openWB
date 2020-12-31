#!/usr/bin/python3
import sys
import os
import time
import json
import urllib.request
import avmcommon
#from urllib.parse import urlparse
named_tuple = time.localtime() # getstruct_time
time_string = time.strftime("%m/%d/%Y, %H:%M:%S avmhomeautomation watt.py", named_tuple)
devicenumber=str(sys.argv[1])
fritzboxAddress = str(sys.argv[2]) # IP or hostname (e.g. "fritz.box")
switchname = str(sys.argv[5])
username = str(sys.argv[6])
password = str(sys.argv[7])
# needs to be configurable
file_string = '/var/www/html/openWB/ramdisk/smarthome_device_' + str(devicenumber) + '_avmhomeautomation.log'
file_stringsessionid = '/var/www/html/openWB/ramdisk/smarthome_device_' + str(devicenumber) + '_sessionid'
sessionid = '0000000000000000'
if os.path.isfile(file_stringsessionid):
    f = open(file_stringsessionid, 'r')
    sessionid = f.read()
    f.close()

try:
    if os.path.isfile(file_string):
        f = open( file_string , 'a')
    else:
        f = open( file_string , 'w') 
        print ('%s devicenr %s %s on' % (time_string,devicenumber,url),file=f)
        f.close()
except IOError:
    pass

baseurl='http://' + fritzboxAddress
sessionid = avmcommon.getAVMSessionID(
        baseurl, 
        previoussessionid=sessionid,
        username=username,
        password=password)


switch = avmcommon.getDevicesDict(baseurl, sessionid)[switchname]
aktpower = switch['power']
if aktpower > 50:
    relais = 1
else:
    relais = 0
powerc = 0
answer = '{"power":' + str(aktpower) + ',"powerc":' + str(powerc) + ',"on":' + str(relais) + '} '
f1 = open('/var/www/html/openWB/ramdisk/smarthome_device_ret' + str(devicenumber), 'w')
json.dump(answer,f1)
f1.close()
