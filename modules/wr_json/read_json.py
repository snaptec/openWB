#!/usr/bin/env python3

import requests
import sys
import traceback
import jq
from datetime import datetime, timezone
import os

Debug         = int(os.environ.get('debug'))
myPid         = str(os.getpid())

jsonurl = str(sys.argv[1])

jsonwatt = str(sys.argv[2])
jsonkwh = str(sys.argv[3])
numpv = int(str(sys.argv[4]))

RAMDISKDIR='/var/www/html/openWB/ramdisk/'

def DebugLog(message):
	local_time = datetime.now(timezone.utc).astimezone()
	print(local_time.strftime(format = "%Y-%m-%d %H:%M:%S") + ": PID: "+ myPid +": " + message)



if Debug >= 2:
	DebugLog('PV' + str(numpv) + ' JQ Watt: ' + jsonwatt)
	DebugLog('PV' + str(numpv) + ' JQ Wh  : ' + jsonkwh)
	DebugLog('PV' + str(numpv) + ' JQ numpv  : ' + str(numpv))


response = requests.get(jsonurl, timeout=5).json()
if Debug>=2:
        DebugLog('JSON Response: ' + str(response))
try:
	watt = jq.compile(jsonwatt).input(response).first()
	watt=int(watt)
	if watt >= 0:
		watt = watt*(-1)
	if numpv == 1:
		with open(RAMDISKDIR + "pvwatt", "w") as f:
			f.write(str(watt))
	else:
		with open(RAMDISKDIR + "pv" + str(numpv) + "watt" , "w") as f:
			f.write(str(watt))
except:
	traceback.print_exc()
	exit(1)
if Debug >= 1:
	DebugLog('PV' + str(numpv) + 'Watt: ' + str(watt))

try:
	if jsonkwh != "":
		kwh = jq.compile(jsonkwh).input(response).first()
	else:
		kwh = 0
	if numpv == 1:
		with open(RAMDISKDIR + "pvkwh", "w") as f:
			f.write(str(kwh))
	else:
		with open(RAMDISKDIR + "pv" + str(numpv) + "kwh" , "w") as f:
			f.write(str(kwh))
except:
	traceback.print_exc()
	exit(1)
if Debug >= 1:
	DebugLog('PV' + str(numpv) + 'kWh: ' + str(kwh))

exit(0)
