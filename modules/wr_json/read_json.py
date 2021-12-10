#!/usr/bin/env python3

import re
import requests
import subprocess
import sys
import traceback

num = int(sys.argv[1])
wrjsonurl = str(sys.argv[2])
wrjsonkwh = str(sys.argv[3]).replace(".", "")
wrjsonwatt = str(sys.argv[4]).replace(".", "")

if num == 1:
    file_ext = ""
elif num == 2:
    file_ext = "2"

regex = '^[-+]?[0-9]+\.?[0-9]*$'
answer = requests.get(wrjsonurl, timeout=5).json()
try:
    pvwatt = int(answer[wrjsonwatt])
except:
    traceback.print_exc()
# Wenn WR aus bzw. im Standby (keine Antwort), ersetze leeren Wert durch eine 0
if re.search(regex, pvwatt) == None:
    msg = "'PV"+str(file_ext)+"Watt Not Numeric: "+str(pvwatt)+" . Check if Filter is correct or WR is in standby'"
    subprocess.run(['bash', '-c', 'source /var/www/html/openWB/helperFunctions.sh; openwbDebugLog "PV" 1 '+msg])
    pvwatt = 0

if pvwatt > 5:
    pvwatt = pvwatt*-1
with open("/var/www/html/openWB/ramdisk/pv"+file_ext+"watt", "w") as f:
    f.write(str(pvwatt))

if wrjsonkwh != "":
    try:
        pvkwh = answer[wrjsonkwh]
    except:
        traceback.print_exc()
    if re.search(regex, pvkwh) == None:
        msg = "'PV"+str(file_ext)+"kWh Not Numeric: "+str(pvkwh)+" . Check if Filter is correct or WR is in standby'"
        subprocess.run(['bash', '-c', 'source /var/www/html/openWB/helperFunctions.sh; openwbDebugLog "PV" 1 '+msg])
        with open("/var/www/html/openWB/ramdisk/pvkwh", "r") as f:
            pvkwh = f.read()
else:
    msg = "'PV"+str(file_ext)+"kWh NoFilter is set'"
    subprocess.run(['bash', '-c', 'source /var/www/html/openWB/helperFunctions.sh; openwbDebugLog "PV" 2 '+msg])
    pvkwh = 0

with open("/var/www/html/openWB/ramdisk/pv"+file_ext+"kwh", "w") as f:
    f.write(str(pvkwh))
