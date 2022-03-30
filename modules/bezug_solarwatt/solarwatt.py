#!/usr/bin/env python3
from typing import List
import logging
import requests
import sys

from helpermodules.cli import run_using_positional_cli_args

log = logging.getLogger("Solarwatt EVU")


def update(solarwattmethod: int, speicher1_ip: str, speicher1_ip2: str):
    log.debug('Solarwatt Methode: ' + str(solarwattmethod))
    log.debug('Solarwatt IP1: ' + speicher1_ip)
    log.debug('Solarwatt IP2: ' + speicher1_ip2)

    if solarwattmethod == 0:  # Abruf über Energy Manager
        sresponse = requests.get('http://'+speicher1_ip+'/rest/kiwigrid/wizard/devices', timeout=3).json()
        if len(str(sresponse)) < 10:
            with open("/var/www/html/openWB/ramdisk/wattbezug", "r") as f:
                bezugwatt = f.read()
        else:
            for item in sresponse["result"]["items"].values():
                bezugw = int(item["tagValues"]["PowerConsumedFromGrid"]["value"])

            for item in sresponse["result"]["items"].values():
                einspeisungw = int(item["tagValues"]["PowerOut"]["value"])
            bezugwatt = bezugw - einspeisungw
    if solarwattmethod == 1:  # Abruf über Gateway
        sresponse = requests.get('http://'+speicher1_ip2+':8080/', timeout=3).json()
        bezugwatt = int(sresponse["FData"]["PGrid"])

    log.debug("Netzbezug: "+str(bezugwatt)+" W")
    with open("/var/www/html/openWB/ramdisk/wattbezug", "w") as f:
        f.write(str(bezugwatt))


def main(argv: List[str]):
    run_using_positional_cli_args(update, argv)
