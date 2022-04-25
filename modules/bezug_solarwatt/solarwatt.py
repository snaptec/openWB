#!/usr/bin/env python3
from typing import List
import logging
import requests

from helpermodules.cli import run_using_positional_cli_args

log = logging.getLogger("Solarwatt EVU")


def update(solarwattmethod: int, speicher1_ip: str, speicher1_ip2: str):
    log.debug('Solarwatt Methode: ' + str(solarwattmethod))
    log.debug('Solarwatt IP1: ' + speicher1_ip)
    log.debug('Solarwatt IP2: ' + speicher1_ip2)

    if solarwattmethod == 0:  # Abruf über Energy Manager
        json_response = requests.get('http://'+speicher1_ip+'/rest/kiwigrid/wizard/devices', timeout=3).json()
        if len(str(json_response)) < 10:
            with open("/var/www/html/openWB/ramdisk/wattbezug", "r") as f:
                bezug_watt = f.read()
        else:
            for item in json_response["result"]["items"]:
                try:
                    power_consumed = int(item["tagValues"]["PowerConsumedFromGrid"]["value"])
                    break
                except KeyError:
                    pass
            else:
                raise Exception("Solarwatt konnte keine EVU-Bezugsleistung ermitteln.")

            for item in json_response["result"]["items"]:
                try:
                    power_out = int(item["tagValues"]["PowerOut"]["value"])
                    break
                except KeyError:
                    pass
            else:
                raise Exception("Solarwatt konnte keine EVU-Einspeiseleistung ermitteln.")

            bezug_watt = power_consumed - power_out
    if solarwattmethod == 1:  # Abruf über Gateway
        json_response = requests.get('http://'+speicher1_ip2+':8080/', timeout=3).json()
        bezug_watt = int(json_response["FData"]["PGrid"])

    log.debug("Netzbezug: "+str(bezug_watt)+" W")
    with open("/var/www/html/openWB/ramdisk/wattbezug", "w") as f:
        f.write(str(bezug_watt))


def main(argv: List[str]):
    run_using_positional_cli_args(update, argv)
