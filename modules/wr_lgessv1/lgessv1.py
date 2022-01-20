#!/usr/bin/env python3
from datetime import datetime, timezone
import os
import json
import os.path
import requests
import sys
import traceback

# ess_url: IP/URL des LG ESS V1.0
#
# ess_pass: Passwort, um sich in den LG ESS V1.0 einzuloggen
#            Das Passwort ist standardmäßig die Registrierungsnr.
#            die sich auf dem PCS (dem Hybridwechselrichter und
#            Batteriemanagementsystem) befindet (Aufkleber!). Alter-
#            nativ findet man die Registrierungsnr. in der App unter
#            dem Menüpunkt "Systeminformationen"
#            Mit der Registrierungsnr. kann man sich dann in der
#            Rolle "installer" einloggen.

Debug = int(os.environ.get('debug'))
myPid = str(os.getpid())

lgessv1ip = str(sys.argv[1])
ess_pass = str(sys.argv[2])
ess_api_ver = str(sys.argv[3])
ess_url = "https://"+lgessv1ip


def DebugLog(message):
    local_time = datetime.now(timezone.utc).astimezone()
    print(local_time.strftime(format="%Y-%m-%d %H:%M:%S") + ": PID: " + myPid + ": " + message)


if Debug >= 2:
    DebugLog('Wechselrichter LG IP: ' + lgessv1ip)
    DebugLog('Wechselrichter LG Passwort: ' + ess_pass)
    DebugLog('Wechselrichter LG Version: ' + ess_api_ver)

#
# Flag für unterschiedliche API-Versionen der Firmware
#
if ess_api_ver == "10.2019":
    arr_pos = "13"
else:
    arr_pos = "1"

#
# Prüfen, ob ein Sessionkey in der Ramdisk vorhanden ist. Wenn nicht,
#  z.b. wenn das System neu gestartet wurde, dann wird ein Dummykey an-
#  gelegt
if os.path.isfile("/var/www/html/openWB/ramdisk/ess_session_key"):
    with open("/var/www/html/openWB/ramdisk/ess_session_key", "r") as f:
        # erste Zeile ohne Anhaengen einer neuen Zeile lesen
        session_key = f.readline().strip()
else:
    session_key = " "

#
# JSON-Objekt vom PCS abholen. Es können folgende JSON-Objekte zurück gegeben werden:
#
#  1. Wenn der Sessionkey nicht korrekt bzw. wenn die Session abgelaufen ist, dann wird ein
#     JSON-Objekt mit einem Attribut "auth_key" zurück gegeben
#  2. Der Sessionkey ist gültig, dann erhält man ein JSON-Objekt mit den wichtigsten Attribute.
#     Beispiel JSON-Objekte liegen im Ordner lgessv1/JSON-Beispiele.txt
#
try:
    headers = {'Content-Type': 'application/json', }
    data = json.dumps({"auth_key": session_key})
    response = requests.post(ess_url+'/v1/user/essinfo/home', headers=headers,
                             data=data, verify=False, timeout=5).json()
    authchk = response['auth']
except:
    traceback.print_exc()
    exit(1)
#
# Pruefen, ob Sessionkey ungültig ist, wenn ja, Login und neuen Sessionkey empfangen
#
if authchk == "auth_key failed" or authchk == "auth timeout" or authchk == "":
    try:
        headers = {'Content-Type': 'application/json', }
        data = json.dumps({"password": ess_pass})
        response = requests.put(ess_url+'/v1/login', headers=headers, data=data, verify=False, timeout=5).json()
        session_key = response["auth_key"]
        outjson = {"auth_key": session_key}
    except:
        traceback.print_exc()
        exit(1)
    #
    # aktuelle Daten aus dem PCS auslesen
    #
    headers = {'Content-Type': 'application/json', }
    data = json.dumps(outjson)
    response = requests.post(ess_url+'/v1/user/essinfo/home', headers=headers,
                             data=data, verify=False, timeout=5).json()
    #
    # Sessionkey in der Ramdisk abspeichern
    #
    with open("/var/www/html/openWB/ramdisk/ess_session_key", "w") as f:
        f.write(str(session_key))

#
# JSON-Objekt auswerten
#
try:
    pcs_pv_total_power = response["statistics"]["pcs_pv_total_power"]
except:
    traceback.print_exc()
    exit(1)
#
# Daten für Langzeitlog holen
#
today = datetime.today()
jahr = today.strftime("%Y")
monat = today.strftime("%m")
arr_pos = monat

headers = {'Content-Type': 'application/json', }
data = json.dumps({"auth_key": session_key, "year": str(jahr)})
response = requests.post(ess_url+'/v1/user/graph/pv/year', headers=headers, data=data, verify=False, timeout=5).json()
try:
    pvkwh = response["loginfo"][arr_pos]["total_generation"]
    pvkwh = pvkwh.replace("kwh", "")
    pvkwh = int(pvkwh)
except:
    traceback.print_exc()
    exit(1)
try:
    ekwh = response["loginfo"][arr_pos]["total_Feed_in"]
    ekwh = ekwh.replace("kwh", "")
    ekwh = int(ekwh)
except:
    traceback.print_exc()
    exit(1)
#
# Daten in Ramdisk schreiben
#
# echo $pvkwh > /var/www/html/openWB/ramdisk/pvkwh
# echo $pvkwh > /var/www/html/openWB/ramdisk/pv1kwh_temp
# echo $ekwh > /var/www/html/openWB/ramdisk/einspeisungkwh
if Debug >= 1:
    DebugLog('WR Leistung: ' + "-"+str(pcs_pv_total_power))
with open("/var/www/html/openWB/ramdisk/pvwatt", "w") as f:
    f.write("-"+str(pcs_pv_total_power))

exit(0)
