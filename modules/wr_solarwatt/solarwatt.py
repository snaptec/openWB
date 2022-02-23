#!/usr/bin/env python3
from typing import List
import logging
import requests

from helpermodules.cli import run_using_positional_cli_args


log = logging.getLogger("Solarwatt WR")


def update(speicher1_ip: str):
    log.debug('PV Solarwatt IP:' + speicher1_ip)
    sresponse = requests.get('http://'+speicher1_ip+'/rest/kiwigrid/wizard/devices', timeout=3).json()

    for item in sresponse["result"]["items"].values():
        try:
            pvwatt = int(item["tagValues"]["PowerProduced"]["value"])
            break
        except KeyError:
            pass
    else:
        raise Exception("Solarwatt konnte keine WR-Leistung ermitteln.")
    pvwatt = pvwatt * -1
    log.debug("PV-Leistung: "+str(pvwatt)+" W")
    with open("/var/www/html/openWB/ramdisk/pvwatt", "w") as f:
        f.write(str(pvwatt))


def main(argv: List[str]):
    run_using_positional_cli_args(update, argv)
