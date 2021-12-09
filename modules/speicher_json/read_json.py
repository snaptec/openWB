#!/usr/bin/env python3

import requests
import sys
import traceback
import jq
import re
from datetime import datetime, timezone
import os

Debug         = int(os.environ.get('debug'))
myPid         = str(os.getpid())

renumeric ='^-?[0-9]+$'

battjsonurl = str(sys.argv[1])
battjsonwatt = str(sys.argv[2])
battjsonsoc = str(sys.argv[3])

def DebugLog(message):
	local_time = datetime.now(timezone.utc).astimezone()
	print(local_time.strftime(format = "%Y-%m-%d %H:%M:%S") + ": PID: "+ myPid +": " + message)


numcheck = re.compile(renumeric)


response = requests.get(battjsonurl, timeout=5).json()
if Debug>=2:
	DebugLog(str(response))
try:
	speicherleistung = jq.compile(battjsonwatt).input(response).first()
	if Debug>=1:
		DebugLog('Speicherleistung: ' + str(speicherleistung))
	if not numcheck.match(str(speicherleistung)):
		DebugLog('Speicherleistung nicht numerisch. Bitte Filterausdruck ueberpruefen -->0')
		speicherleistung=0
	speicherleistung = int(speicherleistung)
	with open("/var/www/html/openWB/ramdisk/speicherleistung", "w") as f:
		f.write(str(speicherleistung))
except:
	traceback.print_exc()

try:
	if battjsonsoc != "":
		battsoc = jq.compile(battjsonsoc).input(response).first()
		if Debug>=1:
			DebugLog('SpeicherSoC: ' + str(battsoc))
		if not numcheck.match(str(battsoc)):
			DebugLog('SpeicherSoc nicht numerisch. Bitte Filterausdruck ueberpruefen -->0')
			battsoc=0
		battsoc = int(battsoc)
	else:
		battsoc = 0
		if Debug>=1:
			DebugLog('SpeicherSoC: ' + str(battsoc))
	with open("/var/www/html/openWB/ramdisk/speichersoc", "w") as f:
		f.write(str(battsoc))
except:
	traceback.print_exc()
