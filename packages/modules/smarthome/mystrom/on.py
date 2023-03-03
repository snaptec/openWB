#!/usr/bin/python3
import sys
import time
import urllib.request
named_tuple = time.localtime()  # getstruct_time
time_string = time.strftime("%m/%d/%Y, %H:%M:%S mystrom on.py", named_tuple)
devicenumber = str(sys.argv[1])
ipadr = str(sys.argv[2])
uberschuss = int(sys.argv[3])
urllib.request.urlopen("http://"+str(ipadr)+"/relay?state=1", timeout=3)
