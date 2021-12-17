#!/usr/bin/env python3

from datetime import datetime, timezone
import json
import os
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

Debug = int(os.environ.get('debug'))
myPid = str(os.getpid())


def DebugLog(message):
    local_time = datetime.now(timezone.utc).astimezone()
    print(local_time.strftime(format="%Y-%m-%d %H:%M:%S") + ": PID: " + myPid + ": " + message)


if Debug >= 2:
    DebugLog('Speicher IP: ' + lgessv1ip)
    DebugLog('Speicher Passwort: ' + ess_pass)
    DebugLog('Speicher Version: ' + ess_api_ver)

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
headers = {'Content-Type': 'application/json', }
data = json.dumps({"auth_key": session_key})
response = requests.post(ess_url+'/v1/user/essinfo/home', headers=headers, data=data, verify=False, timeout=5).json()
try:
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
    batconv_power = response["statistics"]["batconv_power"]
except:
    traceback.print_exc()
    exit(1)

try:
    bat_user_soc = response["statistics"]["bat_user_soc"]
    if Debug >= 1:
        DebugLog('SpeicherSoC: ' + str(bat_user_soc))
    if not str(bat_user_soc).isnumeric():
        DebugLog('SpeicherSoc nicht numerisch. -->0')
        bat_user_soc = 0
except:
    traceback.print_exc()
    exit(1)

try:
    is_battery_discharging_ = response["direction"]["is_battery_discharging_"]
except:
    traceback.print_exc()
    exit(1)

#
# Laden bzw. entladen
#
if is_battery_discharging_ == "1":
    batconv_power = batconv_power*-1

#
# Daten für Langzeitlog holen
#
today = datetime.today()
jahr = today.strftime("%Y")
monat = today.strftime("%m")
arr_pos = monat

headers = {'Content-Type': 'application/json', }
data = json.dumps({"auth_key": session_key, "year": str(jahr)})
response = requests.post(ess_url+'/v1/user/graph/batt/year', headers=headers, data=data, verify=False, timeout=5).json()
try:
    speicherikwh = response["loginfo"][arr_pos]["total_charge"]
    speicherikwh = speicherikwh.replace("kwh", "")
    speicherikwh = int(speicherikwh)
    if Debug >= 1:
        DebugLog('Speicher Import: ' + str(speicherikwh))
    if not str(speicherikwh).isnumeric():
        DebugLog('Speicher Import nicht numerisch. -->0')
        speicherikwh = 0
except:
    traceback.print_exc()
    exit(1)

try:
    speicherekwh = response["loginfo"][arr_pos]["total_discharge"]
    speicherekwh = speicherekwh.replace("kwh", "")
    speicherekwh = int(speicherekwh)
    if Debug >= 1:
        DebugLog('Speicher Export: ' + str(speicherekwh))
    if not str(speicherekwh).isnumeric():
        DebugLog('Speicher Export nicht numerisch. -->0')
        speicherekwh = 0
except:
    traceback.print_exc()
    exit(1)
#
# Daten in Ramdisk schreiben
#
# echo $speicherikwh > /var/www/html/openWB/ramdisk/speicherikwh
# echo $speicherekwh > /var/www/html/openWB/ramdisk/speicherekwh
bat_user_soc = int(bat_user_soc)
with open("/var/www/html/openWB/ramdisk/speichersoc", "w") as f:
    f.write(str(bat_user_soc))
with open("/var/www/html/openWB/ramdisk/speicherleistung", "w") as f:
    f.write(str(batconv_power))

exit(0)
