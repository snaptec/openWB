#!/usr/bin/env python3

from datetime import datetime, timezone
import os
import json
import requests
import re
import sys
import time
import traceback

Debug = int(os.environ.get('debug'))
myPid = str(os.getpid())

base_dir = str(sys.argv[1])
speicherpwloginneeded = int(sys.argv[2])
speicherpwuser = str(sys.argv[3])
speicherpwpass = str(sys.argv[4])
speicherpwip = str(sys.argv[5])

ramdiskdir = base_dir+"/ramdisk"
module = "BAT"
logfile = ramdiskdir+"/openWB.log"
cookie_file = ramdiskdir+"/powerwall_cookie.txt"
cookie = ""


def DebugLog(message):
    local_time = datetime.now(timezone.utc).astimezone()
    print(local_time.strftime(format="%Y-%m-%d %H:%M:%S") + ": PID: " + myPid + ": " + message)


def get_value(answer, key, file):
    try:
        value = answer["0"]["Cached_readings"][key]
        with open("/var/www/html/openWB/ramdisk/"+file, "w") as f:
            f.write(str(value))
    except:
        traceback.print_exc()
        exit(1)
    if Debug >= 1:
        DebugLog(file+': ' + str(value))


if Debug >= 2:
    DebugLog('Powerwall IP: ' + speicherpwip)
    DebugLog('Powerwall User: ' + speicherpwuser)
    DebugLog('Powerwall Passwort: ' + speicherpwpass)
    DebugLog('Powerwall Login: ' + speicherpwloginneeded)

if speicherpwloginneeded == 1:
    # delete our login cookie after some time as it may be invalid
    if os.path.isfile(cookie_file) == True:
        edited = os.stat(cookie_file).st_mtime
        now = time.time()
        edit_diff = now - edited
        if edit_diff < 3600:
            DebugLog("Deleting saved login cookie after 1 hour as it may not be valid anymore.")
            os.remove(cookie_file)
    if os.path.isfile(cookie_file) == False:
        # log in and save cookie for later use
        DebugLog("Trying to authenticate...")
        headers = {'Content-Type': 'application/json', }
        data = {"username": "customer", "password": speicherpwpass, "email": speicherpwuser, "force_sm_off": False}
        data = json.dumps(data)
        try:
            response = requests.post('https://'+speicherpwip+'/api/login/Basic', headers=headers, data=data, verify=False, timeout=5)
        except requests.exceptions.RequestException as e:
            DebugLog("Something went wrong. RequestException: "+str(e))
            sys.exit(0)
        else:
            DebugLog("Login successfull.")
            cookie = response.cookies
            with open(cookie_file, "w") as f:
                f.write(str(requests.utils.dict_from_cookiejar(cookie)))
    else:
        DebugLog("Using saved login cookie.")
    with open(cookie_file, "r") as f:
        cookie = f.read()

speicherwatttmp = requests.get("https://"+speicherpwip+"/api/meters/aggregates", cookies=cookie, verify=False, timeout=5).json()
# read current load
try:
    speicherwatt = int(speicherwatttmp["battery"]["instant_power"])
except:
    traceback.print_exc()
    exit(1)
speicherwatt = speicherwatt * -1
ra = '^[-+]?[0-9]+\.?[0-9]*$'
if re.search(ra, speicherwatt) == None:
    speicherwatt = "0"
if Debug >= 1:
    DebugLog('Speicherleistung: ' + str(speicherwatt))
with open("/var/www/html/openWB/ramdisk/speicherleistung", "w") as f:
    f.write(str(speicherwatt))

# read current SoC
speichersoc = requests.get("https://"+speicherpwip+"/api/system_status/soe", cookies=cookie, verify=False, timeout=5).json()
try:
    soc = speichersoc["percentage"]
except:
    traceback.print_exc()
    exit(1)
soc = (soc+0.5)/1
if re.search(ra, soc) == None:
    soc = "0"
if Debug >= 1:
    DebugLog('Speicher Soc: ' + str(soc))
with open("/var/www/html/openWB/ramdisk/speichersoc", "w") as f:
    f.write(str(soc))

exit(0)
