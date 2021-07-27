#!/usr/bin/env python3

import datetime
import json
import os.path
import requests
import sys

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
response = requests.post(ess_url+'/v1/user/essinfo/home', headers=headers, data=data, verify=False, timeout=5)
response = json.loads(response)
authchk = response['auth']
#
# Pruefen, ob Sessionkey ungültig ist, wenn ja, Login und neuen Sessionkey empfangen
#
if authchk == "auth_key failed" or authchk == "auth timeout" or authchk == "":
    headers = {'Content-Type': 'application/json', }
    data = json.dumps({"password": ess_pass})
    response = requests.put(ess_url+'/v1/login', headers=headers, data=data, verify=False, timeout=5)
    response = json.loads(response)
    session_key = response["auth_key"]
    outjson = {"auth_key": session_key}
    #
    # aktuelle Daten aus dem PCS auslesen
    #
    headers = {'Content-Type': 'application/json', }
    data = json.dumps(outjson)
    response = requests.post(ess_url+'/v1/user/essinfo/home', headers=headers, data=data, verify=False, timeout=5)
    #
    # Sessionkey in der Ramdisk abspeichern
    #
    with open("/var/www/html/openWB/ramdisk/ess_session_key", "w") as f:
        f.write(str(session_key))
#
# JSON-Objekt auswerten
#
grid_power = response["statistics"]["grid_power"]
is_grid_selling_ = response["direction"]["is_grid_selling_"]
load_power = response["statistics"]["load_power"]
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
response = requests.post(ess_url+'/v1/user/graph/load/year', headers=headers, data=data, verify=False, timeout=5)
response = json.loads(response)
ikwh = response["loginfo"][arr_pos]["total_purchase"]
ikwh = ikwh.replace("kwh", "")
ikwh = int(ikwh)
loadkwh = response["loginfo"][arr_pos]["total_consumption"]
loadkwh = loadkwh.replace("kwh", "")
loadkwh = int(loadkwh)
#
# Daten in Ramdisk schreiben
#
# echo $ikwh > /var/www/html/openWB/ramdisk/bezugkwh
with open("/var/www/html/openWB/ramdisk/wattbezug", "w") as f:
    f.write(str(grid_power))
