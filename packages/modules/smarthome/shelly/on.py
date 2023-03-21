#!/usr/bin/python3
import sys
import time
import urllib.request
import os
named_tuple = time.localtime()  # getstruct_time
time_string = time.strftime("%m/%d/%Y, %H:%M:%S shelly on.py", named_tuple)
devicenumber = str(sys.argv[1])
ipadr = str(sys.argv[2])
uberschuss = int(sys.argv[3])
gen = "1"
try:
    chan = int(sys.argv[4])
except Exception:
    chan = 0
shaut = int(sys.argv[5])
user = str(sys.argv[6])
pw = str(sys.argv[7])
fbase = '/var/www/html/openWB/ramdisk/smarthome_device_ret.'
fnameg = fbase + str(ipadr) + '_shelly_infog'
if os.path.isfile(fnameg):
    with open(fnameg, 'r') as f:
        gen = str(f.read())
else:
    gen = "1"
if (chan == 0):
    url = "http://" + str(ipadr) + "/relay/0?turn=on"
#    urllib.request.urlopen("http://"+str(ipadr)+"/relay/0?turn=on",
#                           timeout=3)
else:
    chan = chan - 1
    url = "http://" + str(ipadr) + "/relay/" + str(chan) + "?turn=on"
#   urllib.request.urlopen("http://"+str(ipadr)+"/relay/" + str(chan) +
#                           "?turn=on", timeout=3)
if (shaut == 1):
    #  print("Shelly on" + str(shaut) + user + pw)
    passman = urllib.request.HTTPPasswordMgrWithDefaultRealm()
    passman.add_password(None, url, user, pw)
    authhandler = urllib.request.HTTPBasicAuthHandler(passman)
    opener = urllib.request.build_opener(authhandler)
    urllib.request.install_opener(opener)
with urllib.request.urlopen(url) as response:
    response.read().decode("utf-8")
