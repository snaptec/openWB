#!/usr/bin/env python3

import requests
import sys
import traceback
import jq
from datetime import datetime, timezone
import os

Debug         = int(os.environ.get('debug'))
myPid         = str(os.getpid())

bezugjsonurl = str(sys.argv[1])

bezugjsonwatt = str(sys.argv[2])
bezugjsonkwh = str(sys.argv[3])
einspeisungjsonkwh = str(sys.argv[4])

def DebugLog(message):
	local_time = datetime.now(timezone.utc).astimezone()
	print(local_time.strftime(format = "%Y-%m-%d %H:%M:%S") + ": PID: "+ myPid +": " + message)



if Debug >= 2:
	DebugLog('JQ Watt: ' + bezugjsonwatt)
	DebugLog('JQ Bezug: ' + bezugjsonkwh)
	DebugLog('JQ Einsp: ' + einspeisungjsonkwh)


response = requests.get(bezugjsonurl, timeout=5).json()
if Debug>=2:
	DebugLog(str(response))

try:
	evuwatt = jq.compile(bezugjsonwatt).input(response).first()
	evuwatt = int(evuwatt)
	with open("/var/www/html/openWB/ramdisk/wattbezug", "w") as f:
		f.write(str(evuwatt))
except:
	traceback.print_exc()
	exit(1)

if Debug >= 1:
	DebugLog('EVU Watt: ' + str(evuwatt))

try:
	if bezugjsonkwh != "":
		evuikwh = jq.compile(bezugjsonkwh).input(response).first()
	else:
		evuikwh = 0
	with open("/var/www/html/openWB/ramdisk/bezugkwh", "w") as f:
		f.write(str(evuikwh))
except:
	traceback.print_exc()
	exit(1)
if Debug >= 1:
	DebugLog('EVU Bezug: ' + str(evuikwh))

try:
	if einspeisungjsonkwh != "":
		evuekwh = jq.compile(einspeisungjsonkwh).input(response).first()
	else:
		evuekwh = 0
	with open("/var/www/html/openWB/ramdisk/einspeisungkwh", "w") as f:
		f.write(str(evuekwh))
except:
	traceback.print_exc()
	exit(1)
if Debug >= 1:
	DebugLog('EVU Einsp: ' + str(evuekwh))

exit(0)
