#!/usr/bin/env python3

from typing import List
import logging
import requests
import sys
import traceback

from helpermodules.cli import run_using_positional_cli_args

log = logging.getLogger("Solarwatt Speicher")


def get_value(key, sresponse):
    value = 0
    try:
        for item in sresponse["result"]["items"]:
            if "tagValues" in sresponse["result"]["items"][item]:
                if key in sresponse["result"]["items"][item]["tagValues"]:
                    if "value" in sresponse["result"]["items"][item]["tagValues"][key]:
                        value = int(sresponse["result"]["items"][item]["tagValues"][key]["value"])
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
        sresponse = requests.get('http://'+speicher1_ip+'/rest/kiwigrid/wizard/devices', timeout=5).json()
        if len(str(sresponse)) < 10:
            sys.exit(1)

        speichere = get_value("PowerConsumedFromStorage", sresponse)
        speicherein = get_value("PowerOutFromStorage", sresponse)
        speicheri = get_value("PowerBuffered", sresponse)
        speicherleistung = int((speichere + speicherein - speicheri) * -1)
        speichersoc = get_value("StateOfCharge", sresponse)

    elif solarwattmethod == 1:  # Abruf über Gateway
        sresponse = requests.get('http://'+speicher1_ip2+':8080/', timeout=3).json()
        if len(str(sresponse)) < 10:
            sys.exit(1)
        ibat = sresponse["FData"]["IBat"]
        vbat = sresponse["FData"]["VBat"]

        speicherleistung = ibat * vbat
        speicherleistung = int(speicherleistung / (-1))
        speichersoc = int(sresponse["SData"]["SoC"])
        log.debug('SpeicherSoC: ' + str(speichersoc))
        if not str(speichersoc).isnumeric():
            log.debug('SpeicherSoc nicht numerisch. -->0')
            speichersoc = 0
    else:
        raise Exception("Unbekannte Abrufmethode fuer Solarwatt")

    log.debug("Speicherleistung: "+str(speicherleistung)+" W")
    with open("/var/www/html/openWB/ramdisk/speicherleistung", "w") as f:
        f.write(str(speicherleistung))
    log.debug("SpeicherSoC: "+str(speichersoc)+" %")
    with open("/var/www/html/openWB/ramdisk/speichersoc", "w") as f:
        f.write(str(speichersoc))


def main(argv: List[str]):
    run_using_positional_cli_args(update, argv)
