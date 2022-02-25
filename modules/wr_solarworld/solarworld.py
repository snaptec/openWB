#!/usr/bin/env python3
from typing import List
import logging
import re
import requests
import traceback

from helpermodules.cli import run_using_positional_cli_args

log = logging.getLogger("Solarworld WR")


def update(solarworld_emanagerip: str):
    log.debug('PV Solarworld IP:' + solarworld_emanagerip)

    # Auslesen eines Solarworld eManagers über die integrierte JSON-API
    emanagerantwort = requests.get(
        "http://"+solarworld_emanagerip+"/rest/solarworld/lpvm/powerAndBatteryData", timeout=3).json()

    try:
        wr_watt = int(emanagerantwort["PowerTotalPV"])
    except:
        traceback.print_exc()
        exit(1)

    # wenn eManager aus bzw. keine Antwort ersetze leeren Wert durch eine 0
    ra = '^-?[0-9]+$'

    if re.search(ra, str(wr_watt)) == None:
        wr_watt = 0

    # PV ezeugte Leistung muss negativ sein
    pvwatt = 0 - wr_watt
    log.debug("PV-Leistung: "+str(pvwatt)+" W")
    with open("/var/www/html/openWB/ramdisk/pvwatt", "w") as f:
        f.write(str(pvwatt))


def main(argv: List[str]):
    run_using_positional_cli_args(update, argv)
