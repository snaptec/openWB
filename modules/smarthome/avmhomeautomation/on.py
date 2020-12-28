#!/usr/bin/python3
import sys
import os
import time
import json
import urllib.request
import login
import credentials

#from urllib.parse import urlparse
named_tuple = time.localtime() # getstruct_time
time_string = time.strftime("%m/%d/%Y, %H:%M:%S avmhomeautomation on.py", named_tuple)
devicenumber=str(sys.argv[1])
url=str(sys.argv[4])
# needs to be configurable
file_string = '/var/www/html/openWB/ramdisk/smarthome_device_' + str(devicenumber) + '_avmhomeautomation.log'
file_stringsessionid = '/var/www/html/openWB/ramdisk/smarthome_device_' + str(devicenumber) + '_sessionid'
file_stringuser= '/var/www/html/openWB/ramdisk/smarthome_device_' + str(devicenumber) + '_user'
file_stringpass= '/var/www/html/openWB/ramdisk/smarthome_device_' + str(devicenumber) + '_pass'
username = credentials.username
password = credentials.password
sessionid = '0000000000000000'
if os.path.isfile(file_stringsessionid):
    f = open(file_stringsessionid, 'r')
    sessionid = f.read()
    f.close()

if os.path.isfile(file_stringuser):
    f = open(file_stringsessionid, 'r')
    username = f.read()
    f.close()

if os.path.isfile(file_stringpass):
    f = open(file_stringsessionid, 'r')
    password = f.read()
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

if username == '' or password == '':
    sys.exit()

baseurl='http://fritz.box'
sessionid = login.getAVMSessionID(
        baseurl, 
        previoussessionid=sessionid,
        username=username,
        password=password)

try:
    f = open(file_stringsessionid, 'w')
    print ('%s' % (sessionid),file=f)
    f.close()
except IOError:
    pass

baseurl += "/webservices/homeautoswitch.lua?sid="+sessionid+"&switchcmd="

getswitchlisturl=baseurl+"getswitchlist"
getswitchlistResponseBody = str(urllib.request.urlopen(getswitchlisturl).read(), "utf-8").strip()
switchIDs = getswitchlistResponseBody.split(",")
for id in switchIDs:
    getswitchnameurl=baseurl+"getswitchname&ain=" + id
    foundswitchname = str(urllib.request.urlopen(getswitchnameurl).read(), "utf-8").strip()
    if foundswitchname == switchname:
        setswitchonurl=baseurl+"setswitchon&ain=" + id
        urllib.request.urlopen(setswitchonurl)
        sys.exit()

