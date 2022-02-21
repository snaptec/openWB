#!/usr/bin/env python3
from datetime import datetime, timezone
import os
import json
import os.path
from urllib.error import HTTPError
import requests
import sys
import traceback

# Beispiel JSON-Objekte liegen im Ordner lgessv1/JSON-Beispiele.txt
# lg_ess_url:  IP/URL des LG ESS V1.0
# lg_ess_pass: Passwort, um sich in den LG ESS V1.0 einzuloggen
#              Das Passwort ist standardmäßig die Registrierungsnr.
#              die sich auf dem PCS (dem Hybridwechselrichter und
#              Batteriemanagementsystem) befindet (Aufkleber!). Alter-
#              nativ findet man die Registrierungsnr. in der App unter
#              dem Menüpunkt "Systeminformationen"
#              Mit der Registrierungsnr. kann man sich dann in der
#              Rolle "installer" einloggen.

Debug = int(os.environ.get('debug'))
myPid = str(os.getpid())

lg_ess_ip = str(sys.argv[1])
lg_ess_pass = str(sys.argv[2])
lg_ess_api_ver = str(sys.argv[3])
lg_ess_url = "https://"+lg_ess_ip


def DebugLog(message):
    local_time = datetime.now(timezone.utc).astimezone()
    print(local_time.strftime(format="%Y-%m-%d %H:%M:%S") + ": PID: " + myPid + ": " + message)


if Debug >= 2:
    DebugLog('Wechselrichter LG IP: ' + lg_ess_ip)
    DebugLog('Wechselrichter LG Passwort: ' + lg_ess_pass)
    DebugLog('Wechselrichter LG Version: ' + lg_ess_api_ver)

# Prüfen, ob ein Sessionkey in der Ramdisk vorhanden ist. Wenn nicht,
#  z.b. wenn das System neu gestartet wurde, dann wird ein Dummykey an-
#  gelegt
if os.path.isfile("/var/www/html/openWB/ramdisk/ess_session_key"):
    with open("/var/www/html/openWB/ramdisk/ess_session_key", "r") as f:
        # erste Zeile ohne Zeilenumbruch lesen
        session_key = f.readline().strip()
else:
    session_key = " "

auth_check = "not done"
try:
    headers = {'Content-Type': 'application/json', }
    data = json.dumps({"auth_key": session_key})
    response = requests.post(lg_ess_url+'/v1/user/essinfo/home', headers=headers,
                             data=data, verify=False, timeout=5).json()
    if Debug >= 2:
        DebugLog("response: " + str(response))
    # ToDo: check http status by calling response.raise_for_status() on plain response
    auth_check = response['auth']
except KeyError:
    # missing "auth" in response indicates success
    auth_check = ""
    pass

# Prüfen, ob Sessionkey ungültig ist, wenn ja, Login und neuen Sessionkey empfangen
if auth_check == "auth_key failed" or auth_check == "auth timeout" or auth_check == "not done":
    try:
        headers = {'Content-Type': 'application/json', }
        data = json.dumps({"password": lg_ess_pass})
        response = requests.put(lg_ess_url+'/v1/login', headers=headers, data=data, verify=False, timeout=5).json()
        if Debug >= 2:
            DebugLog("response: " + str(response))
        session_key = response["auth_key"]
        outjson = {"auth_key": session_key}
    except (HTTPError, KeyError):
        DebugLog("login failed! check password!")
        traceback.print_exc()
        exit(1)
    # aktuelle Daten aus dem PCS auslesen
    headers = {'Content-Type': 'application/json', }
    data = json.dumps(outjson)
    response = requests.post(lg_ess_url+'/v1/user/essinfo/home', headers=headers,
                             data=data, verify=False, timeout=5).json()
    # Sessionkey in der Ramdisk abspeichern
    with open("/var/www/html/openWB/ramdisk/ess_session_key", "w") as f:
        f.write(str(session_key))

# JSON-Objekt auswerten
pv_total_power = int(float(response["statistics"]["pcs_pv_total_power"])) * -1

if Debug >= 1:
    DebugLog('WR Leistung: ' + str(pv_total_power))
# Daten in Ramdisk schreiben
with open("/var/www/html/openWB/ramdisk/pvwatt", "w") as f:
    f.write(str(pv_total_power))
