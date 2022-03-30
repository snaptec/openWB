#!/usr/bin/env python3

import logging
from typing import List

import requests
import traceback

from helpermodules.cli import run_using_positional_cli_args

log = logging.getLogger("Kostal-Piko")


def update(wrkostalpikoip: str, speichermodul: str):
    log.debug('Kostal Piko IP: ' + wrkostalpikoip)
    log.debug('Kostal Piko Speicher: ' + speichermodul)
    # Auslesen eines Kostal Piko WR über die integrierte API des WR mit angeschlossenem Eigenverbrauchssensor.

    params = (
        ('dxsEntries', ['33556736', '251658753', '83887106', '83887362', '83887618']),
    )
    pvwatttmp = requests.get('http://'+wrkostalpikoip+'/api/dxs.json', params=params, timeout=3).json()
    # aktuelle Ausgangsleistung am WR [W]
    try:
        pvwatt = int(pvwatttmp["dxsEntries"][0]["value"])
    except:
        traceback.print_exc()
        exit(1)
    log.debug('Leistung WR: ' + str(pvwatt))

    if pvwatt > 5:
        pvwatt = pvwatt*-1

    # zur weiteren Verwendung im Webinterface
    with open("/var/www/html/openWB/ramdisk/pvwatt", "w") as f:
        f.write(str(pvwatt))
    # Gesamtzählerstand am WR [kWh]
    try:
        pvkwh = int(pvwatttmp["dxsEntries"][1]["value"])
    except:
        traceback.print_exc()
        exit(1)
    log.debug('Zählerstand WR: ' + str(pvkwh))

    pvkwh = pvkwh*1000
    # zur weiteren Verwendung im Webinterface
    with open("/var/www/html/openWB/ramdisk/pvkwh", "w") as f:
        f.write(str(pvkwh))

    try:
        bezugw1 = int(pvwatttmp["dxsEntries"][2]["value"])
    except:
        traceback.print_exc()
        exit(1)
    log.debug('Leistung L1: ' + str(bezugw1))

    try:
        bezugw2 = int(pvwatttmp["dxsEntries"][3]["value"])
    except:
        traceback.print_exc()
        exit(1)
    log.debug('Leistung L2: ' + str(bezugw2))

    try:
        bezugw3 = int(pvwatttmp["dxsEntries"][4]["value"])
    except:
        traceback.print_exc()
        exit(1)
    log.debug('Leistung L3: ' + str(bezugw3))

    if speichermodul == "speicher_bydhv":
        with open("/var/www/html/openWB/ramdisk/speicherleistung", "r") as f:
            speicherleistung = f.read()
        wattbezug = bezugw1+bezugw2+bezugw3+pvwatt+int(speicherleistung)
    else:
        wattbezug = bezugw1+bezugw2+bezugw3+pvwatt

    with open("/var/www/html/openWB/ramdisk/wattbezug", "w") as f:
        f.write(str(wattbezug))
    log.debug('Watt: ' + str(wattbezug))
    bezuga1 = round((bezugw1 / 225), 2)
    bezuga2 = round((bezugw2 / 225), 2)
    bezuga3 = round((bezugw3 / 225), 2)
    with open("/var/www/html/openWB/ramdisk/bezuga1", "w") as f:
        f.write(str(bezuga1))
    with open("/var/www/html/openWB/ramdisk/bezuga2", "w") as f:
        f.write(str(bezuga2))
    with open("/var/www/html/openWB/ramdisk/bezuga3", "w") as f:
        f.write(str(bezuga3))
    log.debug('Strom L1: ' + str(bezuga1))
    log.debug('Strom L2: ' + str(bezuga2))
    log.debug('Strom L3: ' + str(bezuga3))


def main(argv: List[str]):
    run_using_positional_cli_args(update, argv)
