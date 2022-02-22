#!/usr/bin/env python3
import logging
import os
import json
import os.path
from urllib.error import HTTPError
import requests
import traceback
from typing import List

from helpermodules.cli import run_using_positional_cli_args

log = logging.getLogger("LG")

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


def update(lg_ess_ip: str, lg_ess_pass: str, lg_ess_api_ver: str):
    lg_ess_ip = lg_ess_ip
    lg_ess_pass = lg_ess_pass
    lg_ess_api_ver = lg_ess_api_ver
    lg_ess_url = "https://"+lg_ess_ip

    log.debug('Speicher IP: ' + lg_ess_ip)
    log.debug('Speicher Passwort: ' + lg_ess_pass)
    log.debug('Speicher Version: ' + lg_ess_api_ver)

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
        log.debug("response: " + str(response))
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
            log.debug("response: " + str(response))
            session_key = response["auth_key"]
            outjson = {"auth_key": session_key}
        except (HTTPError, KeyError):
            log.debug("login failed! check password!")
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
    battery_power = int(float(response["statistics"]["batconv_power"]))
    is_battery_discharging_ = response["direction"]["is_battery_discharging_"]
    if is_battery_discharging_ == "1":
        battery_power = battery_power * -1
    try:
        bat_user_soc = int(float(response["statistics"]["bat_user_soc"]))
    except ValueError:
        log.debug('SpeicherSoc nicht numerisch. --> 0')
        bat_user_soc = 0

    log.debug('Speicher Leistung: ' + str(battery_power))
    log.debug('Speicher SoC: ' + str(bat_user_soc))
    # Daten in Ramdisk schreiben
    with open("/var/www/html/openWB/ramdisk/speichersoc", "w") as f:
        f.write(str(bat_user_soc))
    with open("/var/www/html/openWB/ramdisk/speicherleistung", "w") as f:
        f.write(str(battery_power))


def main(argv: List[str]):
    run_using_positional_cli_args(update, argv)
