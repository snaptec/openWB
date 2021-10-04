#!/usr/bin/env python3

import datetime
import json
import requests
import os
import sys
import time
import traceback

Debug         = int(os.environ.get('debug'))
myPid         = str(os.getpid())

base_dir = str(sys.argv[1])
speicherpwloginneeded = int(sys.argv[2])
speicherpwuser = str(sys.argv[3])
speicherpwpass = str(sys.argv[4])
speicherpwip = str(sys.argv[5])

ramdiskdir = base_dir+"/ramdisk"
module = "EVU"
logfile = ramdiskdir+"/openWB.log"
cookie_file = ramdiskdir+"/powerwall_cookie.txt"
cookie = ""


def DebugLog(msg):
    if Debug > 0:
        timestamp = datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")
        if Debug == 2:
            with open(logfile, "a") as f:
                f.write(str(timestamp)+": "+str(module)+": PID:"+myPid+": "+msg)
        else:
            with open(logfile, "a") as f:
                f.write(str(timestamp)+": "+str(module)+": "+msg)


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
        headers = {'Content-Type': 'application/json',}
        data = {"username":"customer","password":speicherpwpass, "email":speicherpwuser,"force_sm_off":False}
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

answer = requests.get("https://"+speicherpwip+"/api/meters/aggregates", cookies = cookie, verify=False, timeout=5).json()
try:
    evuwatt=int(answer["site"]["instant_power"])
except:
    traceback.print_exc()
    exit(1)
if Debug >= 1:
    DebugLog('Leistung: ' + str(evuwatt))
with open("/var/www/html/openWB/ramdisk/wattbezug", "w") as f:
    f.write(str(evuwatt))

try:
    evuikwh=answer["site"]["energy_imported"]
except:
    traceback.print_exc()
    exit(1)
if Debug >= 1:
    DebugLog('Bezug: ' + str(evuikwh))
with open("/var/www/html/openWB/ramdisk/bezugkwh", "w") as f:
    f.write(str(evuikwh))

try:
    evuekwh=answer["site"]["energy_exported"]
except:
    traceback.print_exc()
    exit(1)
if Debug >= 1:
    DebugLog('Einspeisung: ' + str(evuekwh))
with open("/var/www/html/openWB/ramdisk/einspeisungkwh", "w") as f:
    f.write(str(evuekwh))

answer = requests.get("https://"+speicherpwip+"/api/status", cookies = cookie, verify=False, timeout=5).json()
try:
    powerwallfirmwareversion=int(answer["version"])
except:
    traceback.print_exc()
    exit(1)
if Debug >= 1:
    DebugLog('Version: ' + str(powerwallfirmwareversion))
with open("/var/www/html/openWB/ramdisk/powerwallfirmwareversion", "w") as f:
    f.write(str(powerwallfirmwareversion))

if powerwallfirmwareversion >= 20490:
    answer = requests.get("https://"+speicherpwip+"/api/meters/site", cookies = cookie, verify=False, timeout=5).json()
    get_value(answer, "v_l1n", "evuv1")
    get_value(answer, "v_l2n", "evuv2")
    get_value(answer, "v_l3n", "evuv3")
    get_value(answer, "i_a_current", "bezuga1")
    get_value(answer, "i_b_current", "bezuga2")
    get_value(answer, "i_c_current", "bezuga3")
    get_value(answer, "real_power_a", "bezugw1")
    get_value(answer, "real_power_b", "bezugw2")
    get_value(answer, "real_power_c", "bezugw3")

exit(0)