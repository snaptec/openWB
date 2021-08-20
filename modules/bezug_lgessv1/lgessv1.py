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
lgessv1ip = str(sys.argv[1])
ess_pass = str(sys.argv[2])
ess_api_ver = str(sys.argv[3])
ess_url = "https://"+lgessv1ip

Debug         = int(os.environ.get('debug'))
myPid         = str(os.getpid())

def DebugLog(message):
    local_time = datetime.now(timezone.utc).astimezone()
    print(local_time.strftime(format = "%Y-%m-%d %H:%M:%S") + ": PID: "+ myPid +": " + message)

if Debug >= 2:
    DebugLog('LG IP: ' + lgessv1ip)
    DebugLog('LG Passwort: ' + ess_pass)
    DebugLog('LG Version: ' + ess_api_ver)

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
    response = requests.post(ess_url+'/v1/user/essinfo/home', headers=headers, data=data, verify=False, timeout=5).json()
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
    response = requests.post(ess_url+'/v1/user/essinfo/home', headers=headers, data=data, verify=False, timeout=5).json()
    #
    # Sessionkey in der Ramdisk abspeichern
    #
    with open("/var/www/html/openWB/ramdisk/ess_session_key", "w") as f:
        f.write(str(session_key))
#
# JSON-Objekt auswerten
#
try:
    grid_power = response["statistics"]["grid_power"]
except:
    traceback.print_exc()
    exit(1)
try:
    is_grid_selling_ = response["direction"]["is_grid_selling_"]
except:
    traceback.print_exc()
    exit(1)
if Debug >= 1:
    DebugLog('Imp/Exp: ' + str(is_grid_selling_))
try:
    load_power = response["statistics"]["load_power"]
except:
    traceback.print_exc()
    exit(1)
if is_grid_selling_ == "1":
    grid_power = grid_power*-1

#
# Daten für Langzeitlog holen
#
today = datetime.datetime.today()
jahr = today.strftime("%Y")
monat = today.strftime("%m")
arr_pos = monat

headers = {'Content-Type': 'application/json', }
data = json.dumps({"auth_key": session_key, "year": str(jahr)})
response = requests.post(ess_url+'/v1/user/graph/load/year', headers=headers, data=data, verify=False, timeout=5).json()
try:
    ikwh = response["loginfo"][arr_pos]["total_purchase"]
    ikwh = ikwh.replace("kwh", "")
    ikwh = int(ikwh)
except:
    traceback.print_exc()
    exit(1)
try:
    loadkwh = response["loginfo"][arr_pos]["total_consumption"]
    loadkwh = loadkwh.replace("kwh", "")
    loadkwh = int(loadkwh)
except:
    traceback.print_exc()
    exit(1)
#
# Daten in Ramdisk schreiben
#
# echo $ikwh > /var/www/html/openWB/ramdisk/bezugkwh
with open("/var/www/html/openWB/ramdisk/wattbezug", "w") as f:
    f.write(str(grid_power))
if Debug >= 1:
    DebugLog('Watt: ' + str(grid_power))

exit(0)