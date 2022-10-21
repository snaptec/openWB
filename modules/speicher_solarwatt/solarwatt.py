#!/usr/bin/env python3

from typing import List
import logging
import requests
import sys
import traceback

from helpermodules.cli import run_using_positional_cli_args

log = logging.getLogger("Solarwatt Speicher")


def get_value(key: str, json_response):
    value = 0
    try:
        for item in json_response["result"]["items"]:
            if "tagValues" in item:
                if key in item["tagValues"]:
                    if "value" in item["tagValues"][key]:
                        value = int(item["tagValues"][key]["value"])
                        break
    except:
        traceback.print_exc()
        exit(1)
    return value


def update(solarwattmethod: int, speicher1_ip: str, speicher1_ip2: str):
    log.debug('Speicher Methode: ' + str(solarwattmethod))
    log.debug('Speicher IP1: ' + speicher1_ip)
    log.debug('Speicher IP2: ' + speicher1_ip2)

    if solarwattmethod == 0:  # Abruf über Energy Manager
        json_response = requests.get('http://'+speicher1_ip+'/rest/kiwigrid/wizard/devices', timeout=5).json()
        if len(str(json_response)) < 10:
            sys.exit(1)

        speicher_e = get_value("PowerConsumedFromStorage", json_response)
        speicher_ein = get_value("PowerOutFromStorage", json_response)
        speicher_i = get_value("PowerBuffered", json_response)
        speicher_leistung = int((speicher_e + speicher_ein - speicher_i) * -1)
        speicher_soc = get_value("StateOfCharge", json_response)

    elif solarwattmethod == 1:  # Abruf über Gateway
        json_response = requests.get('http://'+speicher1_ip2+':8080/', timeout=3).json()
        if len(str(json_response)) < 10:
            sys.exit(1)
        speicher_strom = json_response["FData"]["IBat"]
        speicher_spannung = json_response["FData"]["VBat"]

        speicher_leistung = int(speicher_strom * speicher_spannung * -1)
        speicher_soc = int(json_response["SData"]["SoC"])
        log.debug('SpeicherSoC: ' + str(speicher_soc))
        if not str(speicher_soc).isnumeric():
            log.debug('SpeicherSoc nicht numerisch. -->0')
            speicher_soc = 0
    else:
        raise Exception("Unbekannte Abrufmethode für Solarwatt")

    log.debug("Speicherleistung: "+str(speicher_leistung)+" W")
    with open("/var/www/html/openWB/ramdisk/speicherleistung", "w") as f:
        f.write(str(speicher_leistung))
    log.debug("SpeicherSoC: "+str(speicher_soc)+" %")
    with open("/var/www/html/openWB/ramdisk/speichersoc", "w") as f:
        f.write(str(speicher_soc))


def main(argv: List[str]):
    run_using_positional_cli_args(update, argv)
