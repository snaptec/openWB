#!/usr/bin/python3
import sys
import time
import urllib.request
named_tuple = time.localtime()  # getstruct_time
time_string = time.strftime("%m/%d/%Y, %H:%M:%S shelly off.py", named_tuple)
devicenumber = str(sys.argv[1])
ipadr = str(sys.argv[2])
uberschuss = int(sys.argv[3])
try:
    chan = int(sys.argv[4])
except Exception:
    chan = 0
if (chan == 0):
    urllib.request.urlopen("http://"+str(ipadr)+"/relay/0?turn=off",
                           timeout=3)
else:
    chan = chan - 1
    urllib.request.urlopen("http://"+str(ipadr)+"/relay/" + str(chan) +
                           "?turn=off", timeout=3)
